from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
import sys

class LanCapTray(QSystemTrayIcon):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setToolTip("LanCap Messenger")
        
        # Create Menu
        self.menu = QMenu()
        
        self.show_action = QAction("Open LanCap", self)
        self.settings_action = QAction("Settings", self)
        self.quit_action = QAction("Exit", self)
        
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.settings_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)
        
        self.setContextMenu(self.menu)
        
        # Connections
        self.show_action.triggered.connect(self._show_window)
        self.quit_action.triggered.connect(self._quit_app)
        self.activated.connect(self._on_activated)

    def _show_window(self):
        if self.parent():
            self.parent().showNormal()
            self.parent().activateWindow()

    def _quit_app(self):
        if self.parent() and hasattr(self.parent(), 'quit_application'):
            self.parent().quit_application()
        else:
            sys.exit()

    def _on_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            if self.parent():
                if self.parent().isVisible() and reason == QSystemTrayIcon.Trigger:
                    self.parent().hide()
                else:
                    self._show_window()
