from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLabel, QLineEdit, QPushButton, QDialogButtonBox,
                              QFrame)
from PySide6.QtCore import Qt
from src.config import ConfigManager
import socket


class ProfileDialog(QDialog):
    """Dialog for the current user to edit their own profile."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Profile")
        self.setMinimumWidth(340)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # Title
        title = QLabel("Edit Profile")
        title.setProperty("class", "TitleLabel")
        main_layout.addWidget(title)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # Form
        form = QFormLayout()
        form.setSpacing(8)
        form.setLabelAlignment(Qt.AlignRight)

        self.display_name_edit = QLineEdit()
        self.display_name_edit.setPlaceholderText(socket.gethostname())
        self.display_name_edit.setText(ConfigManager.get('display_name', socket.gethostname()))

        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Enter first name")
        self.first_name_edit.setText(ConfigManager.get('first_name', ''))

        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Enter last name")
        self.last_name_edit.setText(ConfigManager.get('last_name', ''))

        self.designation_edit = QLineEdit()
        self.designation_edit.setPlaceholderText("e.g. Software Engineer")
        self.designation_edit.setText(ConfigManager.get('designation', ''))

        form.addRow("Display Name:", self.display_name_edit)
        form.addRow("First Name:", self.first_name_edit)
        form.addRow("Last Name:", self.last_name_edit)
        form.addRow("Designation:", self.designation_edit)
        main_layout.addLayout(form)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)

    def get_values(self):
        return {
            'display_name': self.display_name_edit.text().strip() or socket.gethostname(),
            'first_name': self.first_name_edit.text().strip(),
            'last_name': self.last_name_edit.text().strip(),
            'designation': self.designation_edit.text().strip(),
        }


class PeerDetailDialog(QDialog):
    """Read-only dialog showing another user's full profile details."""

    def __init__(self, peer_data: dict, parent=None):
        super().__init__(parent)
        name = peer_data.get('name', 'Unknown')
        self.setWindowTitle(f"User Details – {name}")
        self.setMinimumWidth(300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Avatar + display name header
        title = QLabel(f"👤  {name}")
        title.setProperty("class", "TitleLabel")
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(8)
        form.setLabelAlignment(Qt.AlignRight)

        first = peer_data.get('first_name', '') or '—'
        last  = peer_data.get('last_name', '')  or '—'
        desg  = peer_data.get('designation', '') or '—'
        ip    = peer_data.get('ip', '—')
        status = peer_data.get('status', 'Available')

        form.addRow("First Name:",  QLabel(first))
        form.addRow("Last Name:",   QLabel(last))
        form.addRow("Designation:", QLabel(desg))
        form.addRow("IP Address:",  QLabel(ip))
        form.addRow("Status:",      QLabel(status))

        layout.addLayout(form)

        btn = QPushButton("Close")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn, alignment=Qt.AlignRight)
