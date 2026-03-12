import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    
    # Simple window for verification
    window = QMainWindow()
    window.setWindowTitle("LanCap Messenger - Setup Verification")
    window.resize(600, 400)
    
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    label = QLabel("🚀 LanCap Environment Ready!")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
    
    sub_label = QLabel("Project structure created. Virtual environment ready.")
    sub_label.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(label)
    layout.addWidget(sub_label)
    
    window.setCentralWidget(central_widget)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
