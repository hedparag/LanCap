from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QTextEdit, QLineEdit, QPushButton, QSplitter, QLabel)
from PySide6.QtCore import Qt
from src.ui.styles import get_main_style

class ChatWindow(QMainWindow):
    def __init__(self, user_name="AVISHEK-NIC"):
        super().__init__()
        self.setWindowTitle(f"{user_name} - Conversation")
        self.resize(350, 450)
        self.setStyleSheet(get_main_style())
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Splitter to separate history and input
        self.splitter = QSplitter(Qt.Vertical)
        
        # Chat History
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setObjectName("ChatTextEdit")
        
        # Bottom area (Toolbar + Input)
        self.bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(self.bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        
        # Drag handle indicator at top of bottom area (emulating standard splitter look)
        drag_handle = QLabel("------------------------")
        drag_handle.setAlignment(Qt.AlignCenter)
        drag_handle.setStyleSheet("color: #A0A0A0; font-size: 8px; background-color: #F0F0F0; padding: 0px;")
        
        # Toolbar
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setObjectName("ChatToolbar")
        toolbar_layout = QHBoxLayout(self.toolbar_widget)
        toolbar_layout.setContentsMargins(4, 2, 4, 2)
        toolbar_layout.setSpacing(5)
        
        # Left Toolbar buttons
        self.btn_font = QPushButton("A")
        self.btn_font.setStyleSheet("font-weight: bold; font-family: serif; font-size: 16px;")
        self.btn_color = QPushButton("A/a") # Substitute icon
        self.btn_emoji = QPushButton("😊")
        self.btn_attach = QPushButton("📎")
        self.btn_folder = QPushButton("📁")
        self.btn_save = QPushButton("💾")
        
        for btn in [self.btn_font, self.btn_color, self.btn_emoji, self.btn_attach, self.btn_folder, self.btn_save]:
            btn.setFixedSize(28, 28)
            btn.setObjectName("ToolButton")
            toolbar_layout.addWidget(btn)
            
        toolbar_layout.addStretch()
        
        # Right Toolbar buttons
        self.btn_history = QPushButton("📋")
        self.btn_network = QPushButton("🌍")
        
        for btn in [self.btn_history, self.btn_network]:
            btn.setFixedSize(28, 28)
            btn.setObjectName("ToolButton")
            toolbar_layout.addWidget(btn)
            
        # Message Input
        self.message_input = QTextEdit()
        self.message_input.setObjectName("ChatInputEdit")
        self.message_input.setFixedHeight(60) # Typical classic size
        
        bottom_layout.addWidget(drag_handle)
        bottom_layout.addWidget(self.toolbar_widget)
        bottom_layout.addWidget(self.message_input)
        
        self.splitter.addWidget(self.chat_history)
        self.splitter.addWidget(self.bottom_widget)
        self.splitter.setSizes([350, 100])
        
        self.layout.addWidget(self.splitter)
