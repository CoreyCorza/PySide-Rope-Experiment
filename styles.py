window_style = """
    QMainWindow {
        background-color: #1e1e1e;
        padding: 0px;
    }
"""

toggle_button = """        
            QPushButton {
                border: 0px;
                border-radius: 6px;
                background-color: #191919;
                text-align: center;
                padding: 2px;

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
        """

video_viewer = """
            QGraphicsView {
                border: none;
                background-color: #0d0d0d;
            }
            QScrollBar:horizontal {
                border: none;
                background: #0d0d0d;
                height: 5px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #2d2d2d;
                min-width: 5px;
                border-radius: 3px;
            }
            QScrollBar:vertical {
                border: none;
                background: #0d0d0d;
                width: 5px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #2d2d2d;
                min-height: 5px;
                border-radius: 6px;
            }
            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: #0d0d0d;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: #0d0d0d;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #0d0d0d;
            }
        """
        
slider = """  
            QSlider {
                background-color: transparent;
                border: 0px solid black;
                border-radius: 5px;
                height: 10px;
                margin: 0px;
            }
            QSlider::groove:horizontal {
                background-color: #4b4b4b;
                border: 1px transparent;
                height: 3px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
                color: #000000;
                margin: 2px 0;
                border-radius: 1px;
                
            }

            QSlider::handle:horizontal {
                background: #717171;
                border: 0px solid #808080;
                width: 18px;
                margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: transparent;
                border: 2px transparent;
                height: 10px;
                border-radius: 5px;
            } 
            QSlider::add-page:horizontal {
                background-color: transparent;
                border: 0px solid #bbb;
                height: 10px;
                border-radius: 5px;
            }
        """
        
scroll_area = """
            QScrollArea {
                background-color: #141414;  
                border: 0px solid black;
                border-radius: 8px;
            }
        """
player_buttons = """        
            QPushButton {
                border: 0px;
                border-radius: 6px;
                background-color: transparent;
                text-align: center;
                padding: 2px;

            }
            QPushButton:hover {
                background-color: #3d3d3d;
            } 
            QPushButton:pressed {
                background-color: #595959;
            }
            QPushButton:default {
                border-color: none; /* make the default button prominent */
            } 
        """