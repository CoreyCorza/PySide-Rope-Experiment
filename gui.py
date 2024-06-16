from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QVBoxLayout, QSplitter
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import styles as styles
import parameters_panel as params_panel
import video_panel as video_panel
import faces_panel as faces_panel

import os

# ----------------------------- Main Window -----------------------------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        sizex = 1300
        sizey = 900
        x = 1700
        y = 500
        self.setGeometry(x, y, sizex, sizey)
        self.setStyleSheet(styles.window_style)
        # self.resize(1800, 900)



        # Create main window container widget to contain everything I guess
        window_container = QWidget()
        self.setCentralWidget(window_container)
        
        # Create a horizontal layout for the main container
        self.window_layout = QHBoxLayout(window_container)
        self.window_layout.setContentsMargins(4, 0, 0, 0)
        
        # Create a splitter so left side panel width can be adjusted, because fuckit thats why
        splitter = QSplitter(Qt.Horizontal)


        # ------------------------ Left Faces Panel -----------------------------
        self.face_panel = faces_panel.FacesPanel()
        # Add contents to splitter
        splitter.addWidget(self.face_panel)
        
        
        # ------------------------ Middle Video Panel -----------------------------
        # Create middle video panel
        self.middle_panel = QWidget()
        self.middle_layout = QVBoxLayout(self.middle_panel)
        self.middle_layout.setContentsMargins(0, 4, 0, 0)
        self.middle_layout.setSpacing(0)
        self.middle_panel.setLayout(self.middle_layout)

        # Create a horizontal layout for label and button
        popoutin_layout = QHBoxLayout()
        popoutin_layout.setSpacing(0)

        # Add label to the layout to the left
        self.label = QLabel("")
        self.label.setStyleSheet("""QLabel { 
                                    background-color: #0d0d0d; 
                                    border: 0px solid black; 
                                    padding: 2px; 
                                    color: #636363;
                                    border-top-left-radius: 8px; 
                                    border-top-right-radius: 0px;
                                    border-bottom-left-radius: 0px; 
                                    border-bottom-right-radius: 0px;
                                }""")
        self.label.setAlignment(Qt.AlignCenter)

        popoutin_layout.addWidget(self.label, 1)

        # Put a button to the right
        self.pop_out_button = video_panel.PopInOutButton("popout")
        self.pop_out_button.clicked.connect(self.pop_out_panel)
        popoutin_layout.addWidget(self.pop_out_button, 0, Qt.AlignRight)

        # Add the horizontal layout to the middle layout
        self.middle_layout.addLayout(popoutin_layout)

        self.middle_panel_content = video_panel.VideoPanel()
        self.middle_layout.addWidget(self.middle_panel_content)
        self.middle_panel_window = video_panel.VideoPanelWindow(self)

        splitter.addWidget(self.middle_panel)
    
        
        #Add splitter and parameters panel to main layout
        self.window_layout.addWidget(splitter)
        
        
        # ------------------------ Right Parameters Panel -----------------------------
        right_panel = params_panel.ParametersSidePanel(self.window_layout) # Adds itself to the window_layout



    def pop_out_panel(self):
        self.middle_panel_content.setParent(None)
        self.middle_panel_window.set_content(self.middle_panel_content)
        self.middle_panel_window.show()
        self.middle_panel.hide()
        # self.face_panel.setMaximumWidth(self.width() - 200)  # Expand left panel to fill available space
        width = self.width() - 200
        self.face_panel.adjust_on_popout(width)

    def pop_in_panel(self):
        self.middle_panel_window.clear_content()
        self.middle_layout.insertWidget(1, self.middle_panel_content)
        self.middle_panel_window.hide()
        self.middle_panel.show()
        # self.face_panel.adjust_on_popin()
        # self.face_panel.setMaximumWidth(200)  # Restore left panel to fixed width


    def closeEvent(self, event):
        # Override close event of main window to close video panel window as well
        if self.middle_panel_window.isVisible():
            self.middle_panel_window.close()

        event.accept()



def get_icon(icon_name, folder_path=None):
    if folder_path is None:
        folder_path = os.path.join(os.path.dirname(__file__), "media")
    
    icons = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.ico')):
            icon_path = os.path.join(folder_path, file_name)
            icon_name_key = os.path.splitext(file_name)[0]  # Use the file name without extension as the key
            icons[icon_name_key] = QIcon(icon_path)
    
    return icons.get(icon_name)


