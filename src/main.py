import sys
import os

# Add project root to sys.path to resolve 'src' module
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication
from src.ui.windows.main_window import MainWindow
from src.ui.widgets.system_tray import LanCapTray

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Initialize Main Window
    window = MainWindow()
    
    # Initialize System Tray
    logo_path = os.path.join(os.path.dirname(__file__), "ui", "resources", "logo.png")
    tray = LanCapTray(logo_path, window)
    tray.show()
    
    # Show main window
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
