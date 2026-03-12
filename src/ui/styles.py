
def get_main_style():
    return """
    QMainWindow {
        background-color: #F0F0F0;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    QMenuBar {
        background-color: #FFFFFF;
        border-bottom: 1px solid #D4D4D4;
    }
    QMenuBar::item {
        background: transparent;
        padding: 4px 8px;
    }
    QMenuBar::item:selected {
        background: #E5F3FF;
        border-radius: 2px;
    }
    
    #MainHeader {
        background-color: #FFFFFF;
        border-bottom: 1px solid #D4D4D4;
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
    }
    #ToolButton:hover {
        background-color: #E5F3FF;
        border: 1px solid #CCE4F7;
    }
    
    #UserTree {
        background-color: #FFFFFF;
        border: none;
        outline: none;
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
    
    QTreeWidget::branch:has-children:!has-siblings:closed,
    QTreeWidget::branch:closed:has-children:has-siblings {
        border-image: none;
        image: none; /* Add small triangle down */
    }
    
    /* Group Header Style */
    #GroupHeader {
        background-color: #0066CC;
        color: white;
        font-weight: bold;
        padding: 4px;
    }
    
    /* Chat Window Styles */
    #ChatTextEdit {
        border: none;
        background-color: #FFFFFF;
    }
    
    #ChatInputEdit {
        border: none;
        background-color: #FFFFFF;
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
    """

