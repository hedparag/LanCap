
def get_light_style():
    return """
    QMainWindow, QDialog, QMessageBox {
        background-color: #F0F0F0;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #000000;
    }
    
    QMenuBar {
        background-color: #FFFFFF;
        border-bottom: 1px solid #D4D4D4;
        color: #000000;
    }
    QMenuBar::item {
        background: transparent;
        padding: 4px 8px;
    }
    QMenuBar::item:selected {
        background: #E5F3FF;
        border-radius: 2px;
    }
    QMenu {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #D4D4D4;
    }
    QMenu::item:selected {
        background-color: #E5F3FF;
    }
    
    #MainHeader {
        background-color: #FFFFFF;
        border-bottom: 1px solid #D4D4D4;
    }
    #MainHeader QLabel {
        color: #000000;
    }
    
    #NoteInput {
        border: 1px solid #D0D0D0;
        background-color: #F8F8F8;
        padding: 2px;
        color: #777777;
    }
    
    #MainToolbar {
        background-color: #F5F6F7;
        border-bottom: 1px solid #D4D4D4;
    }
    
    #ToolButton {
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 2px;
        color: #000000;
    }
    #ToolButton:hover {
        background-color: #E5F3FF;
        border: 1px solid #CCE4F7;
    }
    
    #UserTree {
        background-color: #FFFFFF;
        border: none;
        outline: none;
        color: #000000;
    }
    #UserTree::item {
        padding: 0px;
    }
    #UserTree::item:hover {
        background-color: #E5F3FF;
    }
    #UserTree::item:selected {
        background-color: #CCE8FF;
        border: 1px dotted #99D1FF;
        color: #000000;
    }
    #UserTree QLabel {
        color: #000000;
    }
    
    QTreeWidget::branch:has-children:!has-siblings:closed,
    QTreeWidget::branch:closed:has-children:has-siblings {
        border-image: none;
        image: none;
    }
    
    #GroupHeader {
        background-color: #0066CC;
        color: white;
        font-weight: bold;
        padding: 4px;
    }
    
    #ChatTextEdit {
        border: none;
        background-color: #FFFFFF;
        color: #000000;
    }
    
    #ChatInputEdit {
        border: none;
        background-color: #FFFFFF;
        color: #000000;
    }
    
    #ChatToolbar {
        background-color: #F0F0F0;
        border-top: 1px solid #A0A0A0;
        border-bottom: 1px solid #A0A0A0;
    }
    
    #ChatToolbar QToolButton {
        background-color: transparent;
        border: 1px solid transparent;
        padding: 2px;
    }
    #ChatToolbar QToolButton:hover {
        background-color: #E5F3FF;
        border: 1px solid #CCE4F7;
    }
    
    QSplitter::handle {
        background-color: #F0F0F0;
        height: 4px;
    }
    
    #DragHandle {
        color: #A0A0A0;
        font-size: 8px;
        background-color: #F0F0F0;
        padding: 0px;
    }
    """

def get_dark_style():
    return """
    QMainWindow, QDialog, QMessageBox {
        background-color: #202020;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #E0E0E0;
    }
    
    QMenuBar {
        background-color: #2D2D30;
        border-bottom: 1px solid #3E3E42;
        color: #E0E0E0;
    }
    QMenuBar::item {
        background: transparent;
        padding: 4px 8px;
    }
    QMenuBar::item:selected {
        background: #3E3E42;
        border-radius: 2px;
    }
    QMenu {
        background-color: #2D2D30;
        color: #E0E0E0;
        border: 1px solid #3E3E42;
    }
    QMenu::item:selected {
        background-color: #3E3E42;
    }
    
    #MainHeader {
        background-color: #2D2D30;
        border-bottom: 1px solid #3E3E42;
    }
    #MainHeader QLabel {
        color: #E0E0E0;
    }
    
    #NoteInput {
        border: 1px solid #3E3E42;
        background-color: #1E1E1E;
        padding: 2px;
        color: #A0A0A0;
    }
    
    #MainToolbar {
        background-color: #252526;
        border-bottom: 1px solid #3E3E42;
    }
    
    #ToolButton {
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 2px;
        color: #E0E0E0;
    }
    #ToolButton:hover {
        background-color: #3E3E42;
        border: 1px solid #007ACC;
    }
    
    QPushButton {
        background-color: #333333;
        color: #E0E0E0;
        border: 1px solid #555555;
        border-radius: 2px;
        padding: 4px;
    }
    QPushButton:hover {
        background-color: #3F3F46;
        border: 1px solid #007ACC;
    }
    
    #UserTree {
        background-color: #1E1E1E;
        border: none;
        outline: none;
        color: #E0E0E0;
    }
    #UserTree::item {
        padding: 0px;
    }
    #UserTree::item:hover {
        background-color: #2A2D2E;
    }
    #UserTree::item:selected {
        background-color: #37373D;
        border: 1px dotted #007ACC;
        color: #FFFFFF;
    }
    #UserTree QLabel {
        color: #E0E0E0;
    }
    
    QTreeWidget::branch:has-children:!has-siblings:closed,
    QTreeWidget::branch:closed:has-children:has-siblings {
        border-image: none;
        image: none;
    }
    
    #GroupHeader {
        background-color: #007ACC;
        color: white;
        font-weight: bold;
        padding: 4px;
    }
    
    #ChatTextEdit {
        border: none;
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    
    #ChatInputEdit {
        border: none;
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    
    #ChatToolbar {
        background-color: #2D2D30;
        border-top: 1px solid #3E3E42;
        border-bottom: 1px solid #3E3E42;
    }
    
    QSplitter::handle {
        background-color: #333333;
        height: 4px;
    }
    
    #DragHandle {
        color: #606060;
        font-size: 8px;
        background-color: #333333;
        padding: 0px;
    }
    """

def get_main_style():
    # Deprecated fallback
    return get_light_style()

