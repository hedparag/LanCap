from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class UserList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("UserList")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.header = QWidget()
        header_layout = QVBoxLayout(self.header)
        
        title = QLabel("CHATS") # More corporate term instead of PEOPLE
        title.setStyleSheet("color: #605E5C; padding-top: 10px; padding-left: 15px; font-weight: 600; font-size: 11px; letter-spacing: 0.5px;")
        
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setPlaceholderText("Search people, groups, or messages...")
        
        self.new_group_btn = QPushButton("+ New Chat")
        self.new_group_btn.setObjectName("NewGroupBtn")
        
        header_layout.addWidget(title)
        header_layout.addWidget(self.search_bar)
        header_layout.addWidget(self.new_group_btn)
        
        self.list = QListWidget()
        
        # Add some mock corporate users
        self.add_user("Alice Johnson", "Engineering Manager", "Online")
        self.add_user("Bob Davidson", "Senior Developer", "Away")
        self.add_user("Charlie Lee", "Product Designer", "Online")
        self.add_user("Marketing Q3 Sync", "Group", "Group")
        
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.list)
        
    def add_user(self, name, title, status):
        # Create a custom widget to make it look professional (Name + Job Title)
        item_widget = QWidget()
        item_layout = QVBoxLayout(item_widget)
        item_layout.setContentsMargins(10, 8, 10, 8)
        item_layout.setSpacing(2)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("color: #323130; font-weight: 600; font-size: 14px; background: transparent;")
        
        status_dot = "🟢" if status == "Online" else "🟡" if status == "Away" else "🔵"
        
        title_label = QLabel(f"{status_dot} {title}")
        title_label.setStyleSheet("color: #605E5C; font-size: 12px; background: transparent;")
        
        item_layout.addWidget(name_label)
        item_layout.addWidget(title_label)
        
        list_item = QListWidgetItem()
        from PySide6.QtCore import QSize
        list_item.setSizeHint(QSize(250, 60))
        
        self.list.addItem(list_item)
        self.list.setItemWidget(list_item, item_widget)
