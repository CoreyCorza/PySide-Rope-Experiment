from PySide6.QtWidgets import QWidget, QVBoxLayout, QVBoxLayout, QScrollArea, QFrame, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Qt
import styles as styles


# ----------------------------- Main Faces Panel -----------------------------

class FacesPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        
        # Haven't start working on this section yet
        # Just a blockout
        
        
        self.resize(300, 0)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        
        
        widget = QScrollArea()
        widget.setStyleSheet(styles.scroll_area)
        widget_layout = QVBoxLayout()
        widget_layout.setAlignment(Qt.AlignTop)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        
        widget.setLayout(widget_layout)

        layout.addWidget(widget)
        
        folder_selector = FolderSelector(widget_layout)
        
        self.setLayout(layout)

    def adjust_on_popout(self, width):
        self.setMaximumWidth(width)
        
    def adjust_on_popin(self):
        self.setMaximumWidth(200)

        


# ----------------------------- UI Elements -----------------------------

class FolderSelector(QWidget):
    def __init__(self, parent_layout=None):
        super().__init__()

        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create the horizontal layout for the text entry and button
        entry_layout = QHBoxLayout()
        entry_layout.setContentsMargins(0, 0, 0, 0)
        entry_layout.setSpacing(0)

        # Create the text entry
        self.text_entry = QLineEdit()
        self.text_entry.setFixedHeight(20)
        self.text_entry.setPlaceholderText("Select a folder...")
        self.text_entry.setStyleSheet("""
            QLineEdit { 
                border: none;
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
            }
        """)

        # Create the button
        self.select_button = QPushButton("Browse")
        self.select_button.clicked.connect(self.open_file_dialog)
        self.select_button.setStyleSheet("""        
            QPushButton {
                border: 0px;
                border-radius: 6px;
                background-color: #282828;
                text-align: center;
                padding: 2px;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
            }
            QPushButton:hover {
                background-color: #232323;
            } 
            QPushButton:pressed {
                background-color: #2c2c2c;
            }
            QPushButton:default {
                border-color: none; /* make the default button prominent */
            } 
        """)

        entry_layout.addWidget(self.text_entry)
        entry_layout.addWidget(self.select_button)

        main_layout.addLayout(entry_layout)
        self.setLayout(main_layout)

        # Add the main layout to the parent layout if provided
        if parent_layout is not None:
            parent_layout.addWidget(self)

    def open_file_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder") 

        if folder_path:
            self.text_entry.setText(folder_path)
