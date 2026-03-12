from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QMenuBar, QMenu, QLabel, QLineEdit,
                              QPushButton, QTreeWidget, QTreeWidgetItem,
                              QMessageBox, QApplication)
from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtCore import Qt, QSize, QPoint
import socket
from src.network.discovery import PeerDiscovery
from src.network.messaging import MessageService
from src.ui.theme_manager import ThemeManager
from src.config import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("LAN Messenger")
        self.resize(300, 550)
        self.setMinimumSize(250, 450)
        
        # Menu Bar
        self.menu_bar = self.menuBar()
        self.messenger_menu = self.menu_bar.addMenu("Messenger")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit_application)
        self.messenger_menu.addAction(exit_action)
        
        # View Menu for Themes
        self.view_menu = self.menu_bar.addMenu("View")
        self.theme_menu = self.view_menu.addMenu("Theme")
        
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)
        
        for theme_name, theme_id in [("System Default", "system"), ("Light", "light"), ("Dark", "dark")]:
            action = QAction(theme_name, self, checkable=True)
            if ThemeManager._current_mode == theme_id:
                action.setChecked(True)
            action.triggered.connect(lambda checked, tid=theme_id: ThemeManager.set_theme(tid))
            theme_group.addAction(action)
            self.theme_menu.addAction(action)
            
        self.tools_menu = self.menu_bar.addMenu("Tools")
        profile_action = QAction("My Profile...", self)
        profile_action.triggered.connect(self.open_profile)
        self.tools_menu.addAction(profile_action)

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
        
        self.system_name = ConfigManager.get('display_name', socket.gethostname())
        first = ConfigManager.get('first_name', '')
        last  = ConfigManager.get('last_name', '')
        full_sub = f"{first} {last}".strip()

        name_status_layout = QHBoxLayout()
        self.name_label = QLabel(self.system_name)
        font_name = self.name_label.font()
        font_name.setBold(True)
        font_name.setPointSize(10)
        self.name_label.setFont(font_name)
        
        self.status_combo = QLabel("Available")
        font_status = self.status_combo.font()
        font_status.setPointSize(8)
        self.status_combo.setFont(font_status)
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
        self.user_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.user_tree.customContextMenuRequested.connect(self.on_tree_context_menu)
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
        
    def on_peer_discovered(self, ip, name, status, first, last, designation):
        icons = ["🌟", "🧭", "🎸", "💽", "🎢"]
        avatar_icon = icons[len(name) % len(icons)]

        if ip in self.peer_items:
            item = self.peer_items[ip]
            item.setData(0, Qt.UserRole, name)
            item.setData(0, Qt.UserRole + 2, {'name': name, 'first_name': first,
                                               'last_name': last, 'designation': designation,
                                               'status': status, 'ip': ip})
            widget = self.user_tree.itemWidget(item, 0)
            if widget:
                name_lbl = widget.findChild(QLabel, "PeerNameLabel")
                sub_lbl  = widget.findChild(QLabel, "PeerSubLabel")
                if name_lbl:
                    name_lbl.setText(f"{name} ({ip})")
                if sub_lbl:
                    full = f"{first} {last}".strip()
                    sub_lbl.setText(full)
                    sub_lbl.setVisible(bool(full))
        else:
            self.add_tree_user(self.group_general, ip, name, first, last, designation, status, avatar_icon)
            
    def on_peer_lost(self, ip):
        if ip in self.peer_items:
            item = self.peer_items[ip]
            # Remove from tree
            index = self.group_general.indexOfChild(item)
            if index >= 0:
                self.group_general.takeChild(index)
            del self.peer_items[ip]
        
    def add_tree_user(self, group, ip, name, first, last, designation, status, avatar_icon):
        item = QTreeWidgetItem(group)
        item.setSizeHint(0, QSize(-1, 48))
        item.setData(0, Qt.UserRole,     name)
        item.setData(0, Qt.UserRole + 1, ip)
        item.setData(0, Qt.UserRole + 2, {'name': name, 'first_name': first,
                                          'last_name': last, 'designation': designation,
                                          'status': status, 'ip': ip})

        widget = QWidget()
        row = QHBoxLayout(widget)
        row.setContentsMargins(5, 2, 5, 2)
        row.setSpacing(6)

        status_lbl = QLabel("👤")
        status_lbl.setStyleSheet("color: #0078D7; font-size: 14px;")

        text_col = QVBoxLayout()
        text_col.setSpacing(1)

        name_lbl = QLabel(f"{name} ({ip})")
        name_lbl.setObjectName("PeerNameLabel")
        name_lbl.setStyleSheet("font-weight: bold; font-size: 12px;")

        full = f"{first} {last}".strip()
        sub_lbl = QLabel(full)
        sub_lbl.setObjectName("PeerSubLabel")
        sub_lbl.setStyleSheet("font-size: 10px;")
        sub_lbl.setVisible(bool(full))

        text_col.addWidget(name_lbl)
        text_col.addWidget(sub_lbl)

        avatar_lbl = QLabel(avatar_icon)
        avatar_lbl.setFixedSize(32, 32)
        avatar_lbl.setAlignment(Qt.AlignCenter)
        avatar_lbl.setStyleSheet("font-size: 18px; border: 1px solid #CCC;")

        row.addWidget(status_lbl)
        row.addLayout(text_col)
        row.addStretch()
        row.addWidget(avatar_lbl)

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

    def open_chat(self, user_name, target_ip, activate=True):
        from src.ui.windows.chat_window import ChatWindow
        self.highlight_peer(target_ip, False) # Clear highlight when opening
        
        if target_ip not in self.active_chats:
            chat_win = ChatWindow(user_name, target_ip, self.messaging)
            self.active_chats[target_ip] = chat_win
            # If we don't activate, just show it silently in background
            if not activate:
                chat_win.show()
            
        chat_win = self.active_chats[target_ip]
        if activate:
            chat_win.show()
            chat_win.raise_()
            chat_win.activateWindow()
        return chat_win

    def on_message_received(self, ip, text):
        user_name = self.discovery.peers.get(ip, {}).get('name', f"Unknown User ({ip})")
        
        chat_win = self.open_chat(user_name, ip, activate=False)
        chat_win.receive_message(text)
        
        # Alert using taskbar highlight and sound, instead of blocking popup
        if not chat_win.isActiveWindow():
            import winsound
            from PySide6.QtWidgets import QApplication
            winsound.MessageBeep(winsound.MB_ICONASTERISK) # Standard Windows notification chime
            QApplication.alert(chat_win, 0) # Flash taskbar indefinitely until clicked
            self.highlight_peer(ip, True)

    def highlight_peer(self, ip, highlight=True):
        if ip in self.peer_items:
            item = self.peer_items[ip]
            widget = self.user_tree.itemWidget(item, 0)
            if widget:
                name_lbl = widget.findChild(QLabel, "PeerNameLabel")
                if name_lbl:
                    if highlight:
                        name_lbl.setStyleSheet("font-weight: bold; font-size: 12px; color: #FF4500;") # Orange-Red
                    else:
                        # Restore default (black for light, white for dark is handled by theme if we clear)
                        name_lbl.setStyleSheet("font-weight: bold; font-size: 12px;")

    def closeEvent(self, event):
        if self.isVisible():
            self.hide()
            event.ignore()

    def quit_application(self):
        # Explicit shutdown from tray or menu
        if hasattr(self, 'discovery'):
            self.discovery.stop()
        if hasattr(self, 'messaging'):
            self.messaging.stop()
        QApplication.quit()

    def on_tree_context_menu(self, pos: QPoint):
        item = self.user_tree.itemAt(pos)
        if not item or item.parent() is None:
            return
        peer_data = item.data(0, Qt.UserRole + 2)
        if not peer_data:
            return

        menu = QMenu(self)
        view_action = menu.addAction("View Profile")
        chat_action = menu.addAction("Start Chat")

        chosen = menu.exec(self.user_tree.mapToGlobal(pos))
        if chosen == view_action:
            from src.ui.windows.profile_dialog import PeerDetailDialog
            dlg = PeerDetailDialog(peer_data, self)
            dlg.exec()
        elif chosen == chat_action:
            self.open_chat(item.data(0, Qt.UserRole), item.data(0, Qt.UserRole + 1))

    def open_profile(self):
        from src.ui.windows.profile_dialog import ProfileDialog
        dlg = ProfileDialog(self)
        if dlg.exec():
            values = dlg.get_values()
            for key, val in values.items():
                ConfigManager.set(key, val)

            self.system_name = values['display_name']
            self.name_label.setText(self.system_name)



            if hasattr(self, 'discovery'):
                self.discovery.set_details(
                    values['display_name'],
                    values['first_name'],
                    values['last_name'],
                    values['designation']
                )


