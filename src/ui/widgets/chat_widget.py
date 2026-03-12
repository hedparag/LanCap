from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTextEdit, QLineEdit, QPushButton, QScrollArea)
from PySide6.QtCore import Qt

class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ChatWidget")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Header
        self.header = QWidget()
        self.header.setObjectName("ChatHeader")
        header_layout = QHBoxLayout(self.header)
        
        # Profile Picture Placeholder
        self.avatar_label = QLabel("👩‍💼")
        self.avatar_label.setStyleSheet("font-size: 24px; padding-right: 10px;")
        
        # User Info
        self.user_info_layout = QVBoxLayout()
        self.user_info_layout.setSpacing(2)
        
        self.user_label = QLabel("Alice Johnson")
        self.user_label.setObjectName("UserNameLabel")
        
        self.status_label = QLabel("🟢 Online • Engineering Manager")
        self.status_label.setObjectName("UserTitleLabel")
        
        self.user_info_layout.addWidget(self.user_label)
        self.user_info_layout.addWidget(self.status_label)
        
        header_layout.addWidget(self.avatar_label)
        header_layout.addLayout(self.user_info_layout)
        header_layout.addStretch()
        
        # Action buttons in header (Call, Video, Info)
        self.call_btn = QPushButton("📞")
        self.call_btn.setObjectName("ActionButton")
        self.video_btn = QPushButton("📹")
        self.video_btn.setObjectName("ActionButton")
        
        header_layout.addWidget(self.call_btn)
        header_layout.addWidget(self.video_btn)
        
        # Message Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("MessageArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.message_layout = QVBoxLayout(self.scroll_content)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        
        # Input Area
        self.input_container = QWidget()
        self.input_container.setObjectName("InputContainer")
        input_layout = QHBoxLayout(self.input_container)
        
        self.attach_btn = QPushButton("📎")
        self.attach_btn.setObjectName("ActionButton")
        self.attach_btn.setToolTip("Attach File")
        
        self.emoji_btn = QPushButton("😊")
        self.emoji_btn.setObjectName("ActionButton")
        self.emoji_btn.setToolTip("Emojis")
        
        self.message_input = QLineEdit()
        self.message_input.setObjectName("MessageInput")
        self.message_input.setPlaceholderText("Type a new message...")
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("SendButton")
        self.send_btn.setCursor(Qt.PointingHandCursor)
        
        input_layout.addWidget(self.attach_btn)
        input_layout.addWidget(self.emoji_btn)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_btn)
        
        # Connections
        self.send_btn.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)
        self.attach_btn.clicked.connect(self.open_file_dialog)
        self.emoji_btn.clicked.connect(self.show_emoji_picker)
        
        # Assembly
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.input_container)
        
        # Mock messages
        self.add_message("Alice Johnson", "Hi there! Just following up on the Q3 rollout plan.", False)
        self.add_message("Me", "Thanks Alice. I've sent the document to the team for review.", True)

    def add_message(self, sender, text, is_me):
        msg_container = QWidget()
        msg_layout = QHBoxLayout(msg_container)
        msg_layout.setContentsMargins(0, 5, 0, 5)
        
        # The main wrapper for the message content
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        
        if is_me:
            msg_layout.addStretch()
            bubble.setObjectName("BubbleMe")
            msg_layout.addWidget(bubble)
        else:
            bubble.setObjectName("BubbleOther")
            
            # Optional: Show avatar for received messages
            sender_avatar = QLabel("👩‍💼")
            sender_avatar.setStyleSheet("font-size: 16px; padding: 0px 5px 0px 0px; margin-top:5px;")
            msg_layout.addWidget(sender_avatar, 0, Qt.AlignTop)
            
            msg_layout.addWidget(bubble)
            msg_layout.addStretch()
            
        self.message_layout.addWidget(msg_container)
        
        # Auto scroll to bottom
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def send_message(self):
        text = self.message_input.text().strip()
        if text:
            self.add_message("Me", text, True)
            self.message_input.clear()

    def open_file_dialog(self):
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Share")
        if file_path:
            self.add_message("Me", f"📄 Shared file: {file_path.split('/')[-1]}", True)

    def show_emoji_picker(self):
        # Multi-line string or more logic could go here
        self.add_message("System", "Emoji Picker: 😊 😂 ❤️ 👍 🔥 🙌", False)
