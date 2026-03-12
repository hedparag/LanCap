from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QMenuBar, QMenu, QLabel, QLineEdit, 
                              QPushButton, QTreeWidget, QTreeWidgetItem)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSize
from src.ui.styles import get_main_style

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
        
        name_status_layout = QHBoxLayout()
        self.name_label = QLabel("PARAG(HED)")
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
        
        self.add_tree_user(group_general, "AVISHEK-NIC", "🌟")
        self.add_tree_user(group_general, "DEBJIT", "🧭")
        self.add_tree_user(group_general, "Dev 12", "🎸")
        self.add_tree_user(group_general, "Lalima Das", "💽")
        self.add_tree_user(group_general, "Rahul", "🌟")
        self.add_tree_user(group_general, "Rakesh", "🎢")
        self.add_tree_user(group_general, "Ratul", "🎸")
        self.add_tree_user(group_general, "Sayan", "💽")
        
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.toolbar_widget)
        self.layout.addWidget(self.user_tree)
        
        # Connections
        self.user_tree.itemDoubleClicked.connect(self.on_user_double_clicked)
        self.active_chats = {} # keep references to chat windows
        
    def add_tree_user(self, group, name, avatar_icon):
        item = QTreeWidgetItem(group)
        item.setSizeHint(0, QSize(-1, 36))
        item.setData(0, Qt.UserRole, name) # Store name to avoid overlapping text
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        
        status_lbl = QLabel("👤")
        status_lbl.setStyleSheet("color: #0078D7; font-size: 14px;")
        name_lbl = QLabel(name)
        
        avatar_lbl = QLabel(avatar_icon)
        avatar_lbl.setFixedSize(32, 32)
        avatar_lbl.setAlignment(Qt.AlignCenter)
        avatar_lbl.setStyleSheet("font-size: 18px; border: 1px solid #CCC;")
        
        layout.addWidget(status_lbl)
        layout.addWidget(name_lbl)
        layout.addStretch()
        layout.addWidget(avatar_lbl)
        
        self.user_tree.setItemWidget(item, 0, widget)

    def on_user_double_clicked(self, item, column):
        # Prevent opening chat for the group header
        if item.parent() is None:
            return
            
        user_name = item.data(0, Qt.UserRole)
        if not user_name:
            return
            
        from src.ui.windows.chat_window import ChatWindow
        
        if user_name not in self.active_chats:
            chat_win = ChatWindow(user_name)
            self.active_chats[user_name] = chat_win
            
        chat_win = self.active_chats[user_name]
        chat_win.show()
        chat_win.raise_()
        chat_win.activateWindow()

    def closeEvent(self, event):
        if self.isVisible():
            self.hide()
            event.ignore()
