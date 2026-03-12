from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QMenuBar, QMenu, QLabel, QLineEdit, 
                              QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSize
import socket
from src.ui.styles import get_main_style
from src.network.discovery import PeerDiscovery
from src.network.messaging import MessageService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("LAN Messenger")
        self.resize(320, 650)
        self.setStyleSheet(get_main_style())
        
        # Menu Bar
        self.menu_bar = self.menuBar()
        self.messenger_menu = self.menu_bar.addMenu("Messenger")
        self.tools_menu = self.menu_bar.addMenu("Tools")
        self.help_menu = self.menu_bar.addMenu("Help")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # User Header Area
        self.header_widget = QWidget()
        self.header_widget.setObjectName("MainHeader")
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        self.status_icon = QLabel("👤")
        self.status_icon.setStyleSheet("font-size: 24px; color: #0078D7;")
        
        user_details_layout = QVBoxLayout()
        user_details_layout.setSpacing(2)
        
        self.system_name = socket.gethostname()
        
        name_status_layout = QHBoxLayout()
        self.name_label = QLabel(self.system_name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #000000;")
        self.status_combo = QLabel("Available")
        self.status_combo.setStyleSheet("color: #333333; font-size: 11px;")
        name_status_layout.addWidget(self.name_label)
        name_status_layout.addStretch()
        name_status_layout.addWidget(self.status_combo)
        
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Type a note")
        self.note_input.setObjectName("NoteInput")
        self.note_input.setFixedHeight(22)
        
        user_details_layout.addLayout(name_status_layout)
        user_details_layout.addWidget(self.note_input)
        
        self.avatar_label = QLabel("💽")
        self.avatar_label.setFixedSize(40, 40)
        self.avatar_label.setStyleSheet("background-color: #333; font-size: 24px;")
        self.avatar_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(self.status_icon)
        header_layout.addLayout(user_details_layout)
        header_layout.addWidget(self.avatar_label)
        
        # Toolbar Area
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setObjectName("MainToolbar")
        toolbar_layout = QHBoxLayout(self.toolbar_widget)
        toolbar_layout.setContentsMargins(4, 4, 4, 4)
        toolbar_layout.setSpacing(4)
        
        # Icons as button text placeholders
        self.btn_chat = QPushButton("💬")
        self.btn_file = QPushButton("📎")
        self.btn_broadcast = QPushButton("📡")
        self.btn_adduser = QPushButton("👤+")
        self.btn_addgroup = QPushButton("👥")
        
        for btn in [self.btn_chat, self.btn_file, self.btn_broadcast, self.btn_adduser, self.btn_addgroup]:
            btn.setFixedSize(36, 32)
            btn.setObjectName("ToolButton")
            btn.setStyleSheet("font-size: 16px;")
            toolbar_layout.addWidget(btn)
        toolbar_layout.addStretch()
        
        # User List (TreeWidget)
        self.user_tree = QTreeWidget()
        self.user_tree.setHeaderHidden(True)
        self.user_tree.setIndentation(15)
        self.user_tree.setObjectName("UserTree")
        self.user_tree.setStyleSheet("font-size: 12px;")
        
        group_general = QTreeWidgetItem(["General"])
        group_general.setBackground(0, Qt.white)
        group_general.setForeground(0, Qt.white)
        # To make it look like the blue header:
        
        # Actually, let's use a widget for the group
        group_widget = QLabel("▼ General")
        group_widget.setObjectName("GroupHeader")
        
        self.user_tree.addTopLevelItem(group_general)
        self.user_tree.setItemWidget(group_general, 0, group_widget)
        group_general.setExpanded(True)
        self.group_general = group_general
        self.peer_items = {} # ip -> QTreeWidgetItem
        
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.toolbar_widget)
        self.layout.addWidget(self.user_tree)
        
        # Connections
        self.user_tree.itemDoubleClicked.connect(self.on_user_double_clicked)
        self.active_chats = {} # keep references to chat windows
        
        # Discovery setup
        self.discovery = PeerDiscovery()
        self.discovery.peer_discovered.connect(self.on_peer_discovered)
        self.discovery.peer_lost.connect(self.on_peer_lost)
        self.discovery.start()
        
        # Messaging setup
        self.messaging = MessageService()
        self.messaging.message_received.connect(self.on_message_received)
        self.messaging.start()
        
    def on_peer_discovered(self, ip, name, status):
        # Default icons based on name slightly for visual variety
        icons = ["🌟", "🧭", "🎸", "💽", "🎢"]
        avatar_icon = icons[len(name) % len(icons)]
        
        if ip in self.peer_items:
            # Update existing
            item = self.peer_items[ip]
            item.setData(0, Qt.UserRole, name)
            widget = self.user_tree.itemWidget(item, 0)
            if widget:
                # Update name label in the custom widget
                name_lbl = widget.findChild(QLabel, "PeerNameLabel")
                if name_lbl:
                    name_lbl.setText(f"{name} ({ip})")
        else:
            # Create new
            self.add_tree_user(self.group_general, ip, name, avatar_icon)
            
    def on_peer_lost(self, ip):
        if ip in self.peer_items:
            item = self.peer_items[ip]
            # Remove from tree
            index = self.group_general.indexOfChild(item)
            if index >= 0:
                self.group_general.takeChild(index)
            del self.peer_items[ip]
        
    def add_tree_user(self, group, ip, name, avatar_icon):
        item = QTreeWidgetItem(group)
        item.setSizeHint(0, QSize(-1, 36))
        item.setData(0, Qt.UserRole, name) # Store name to avoid overlapping text
        item.setData(0, Qt.UserRole + 1, ip) # Store IP address
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        
        status_lbl = QLabel("👤")
        status_lbl.setStyleSheet("color: #0078D7; font-size: 14px;")
        name_lbl = QLabel(f"{name} ({ip})")
        name_lbl.setObjectName("PeerNameLabel")
        
        avatar_lbl = QLabel(avatar_icon)
        avatar_lbl.setFixedSize(32, 32)
        avatar_lbl.setAlignment(Qt.AlignCenter)
        avatar_lbl.setStyleSheet("font-size: 18px; border: 1px solid #CCC;")
        
        layout.addWidget(status_lbl)
        layout.addWidget(name_lbl)
        layout.addStretch()
        layout.addWidget(avatar_lbl)
        
        self.user_tree.setItemWidget(item, 0, widget)
        self.peer_items[ip] = item

    def on_user_double_clicked(self, item, column):
        # Prevent opening chat for the group header
        if item.parent() is None:
            return
            
        user_name = item.data(0, Qt.UserRole)
        target_ip = item.data(0, Qt.UserRole + 1)
        if not user_name or not target_ip:
            return
            
        self.open_chat(user_name, target_ip)

    def open_chat(self, user_name, target_ip):
        from src.ui.windows.chat_window import ChatWindow
        
        if target_ip not in self.active_chats:
            chat_win = ChatWindow(user_name, target_ip, self.messaging)
            self.active_chats[target_ip] = chat_win
            
        chat_win = self.active_chats[target_ip]
        chat_win.show()
        chat_win.raise_()
        chat_win.activateWindow()
        return chat_win

    def on_message_received(self, ip, text):
        user_name = self.discovery.peers.get(ip, {}).get('name', f"Unknown User ({ip})")
        
        # Determine if chat window is already open and visible
        was_visible = ip in self.active_chats and self.active_chats[ip].isVisible()
        
        chat_win = self.open_chat(user_name, ip)
        chat_win.receive_message(text)
        
        if not was_visible:
            # Show an alert dialog only if the chat wasn't already actively opened
            QMessageBox.information(self, "New Message", f"{user_name} says:\n\n{text}")

    def closeEvent(self, event):
        # Make sure to stop discovery and messaging logic
        if hasattr(self, 'discovery'):
            self.discovery.stop()
        if hasattr(self, 'messaging'):
            self.messaging.stop()
        if self.isVisible():
            self.hide()
            event.ignore()

