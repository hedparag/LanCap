from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal

class Sidebar(QWidget):
    nav_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 20, 0, 20)
        self.layout.setSpacing(10)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        # Navigation Buttons
        self.btn_chat = self._create_nav_button("💬", "chat", True)
        self.btn_users = self._create_nav_button("👥", "users")
        self.btn_files = self._create_nav_button("📁", "files")
        
        self.layout.addStretch()
        
        self.btn_settings = self._create_nav_button("⚙️", "settings")
        # Added avatar placeholder at the bottom
        self.btn_profile = self._create_nav_button("👤", "profile")
        
    def _create_nav_button(self, icon_text, name, checked=False):
        btn = QPushButton(icon_text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setFixedSize(48, 48)
        btn.setProperty("nav_name", name)
        
        self.button_group.addButton(btn)
        self.layout.addWidget(btn, 0, Qt.AlignCenter)
        
        btn.clicked.connect(lambda: self.nav_changed.emit(name))
        return btn
