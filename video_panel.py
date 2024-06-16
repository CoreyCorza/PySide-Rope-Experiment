from PySide6.QtWidgets import (QGridLayout, QSlider, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                               QHBoxLayout, QFrame, QLabel, QSizePolicy, QVBoxLayout, QGraphicsView, QGraphicsScene)
from PySide6.QtCore import Qt, QRectF, QPointF, QSize
from PySide6.QtGui import QImage, QPixmap, QMouseEvent, QWheelEvent, QPainter
import gui as gui
import styles as styles


# ----------------------------- Main Video Panel -----------------------------

class VideoPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 4)

        frame = QFrame()
        frame.setStyleSheet(""" QFrame {background-color: #0d0d0d; 
                            border:0px; 
                            border-top-left-radius: 0px; 
                            border-top-right-radius: 0px;
                            border-bottom-left-radius: 0px; 
                            border-bottom-right-radius: 0px;
                            }""" )
        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(0)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_viewer = ImageViewer()
        
        
        
        top_frame_buttons = QHBoxLayout()
        top_frame_buttons.setSpacing(3)
        top_frame_buttons.setAlignment(Qt.AlignCenter)
        frame_layout.addLayout(top_frame_buttons)
        
        
        # Toggle button to switch between modes
        self.toggle_button = QPushButton("Zoom Mode")
        self.toggle_button.setIcon(gui.get_icon("zoom"))
        self.toggle_button.setFixedSize(100, 20)
        self.toggle_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toggle_button.setContentsMargins(0, 0, 0, 0)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet(styles.toggle_button)
        self.toggle_button.clicked.connect(lambda: self.image_viewer.toggleZoom(self.toggle_button))

        mask_button = QPushButton("Mask View")
        mask_button.setIcon(gui.get_icon("mask"))
        mask_button.setFixedSize(100, 20)
        mask_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mask_button.setContentsMargins(0, 0, 0, 0)
        mask_button.setStyleSheet(styles.toggle_button)

        
        
        top_frame_buttons.addWidget(self.toggle_button)
        top_frame_buttons.addWidget(mask_button)
        
        
        
        # frame_layout.addWidget(self.toggle_button, 0, Qt.AlignCenter)
        frame_layout.addWidget(self.image_viewer)
        frame.setLayout(frame_layout)


        
        grid = QWidget()
        grid.setStyleSheet("""QWidget {
            background-color: #131313;  
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 8px;
            border-bottom-left-radius: 8px;
        }""")
       
        # Create a grid layout
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 8)
        grid_layout.setSpacing(0)
        grid.setLayout(grid_layout)
        # grid.setFixedHeight(60)

        
        
        timeline_slider = QSlider(Qt.Horizontal)
        timeline_slider.setStyleSheet(styles.slider)
        timeline_slider.setFixedHeight(20)
        # player_bar_layout.addWidget(timeline_slider)
        # button1 = QPushButton("Button 1")
        grid_layout.addWidget(timeline_slider, 0, 0,)
        
        buttons = QWidget()
        buttons.setStyleSheet("""QWidget {
            background-color: #232323;  
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            border-bottom-left-radius: 8px;
        }""")
        buttons.setFixedSize(250, 25)
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons.setLayout(buttons_layout)
        
        prev_button = PlayerButton(buttons_layout, "prev", 16, 16)
        rec_button = PlayerButton(buttons_layout, "rec", 16, 16)
        stop_button = PlayerButton(buttons_layout, "stop", 12, 12)
        play_button = PlayerButton(buttons_layout, "play", 17, 17)
        next_button = PlayerButton(buttons_layout, "next", 16, 16)

        # Add widgets to the layout
        grid_layout.addWidget(buttons, 1, 0, alignment=Qt.AlignCenter)
        



        
        layout.addWidget(frame)
        layout.addWidget(grid)
        
        
        # layout.addWidget(player_bar)

        self.setLayout(layout)

        # Test Image
        self.image_viewer.setImage("./media/test.jpg") #------------------------------- Test image


# ----------------------------- UI Elements -----------------------------

class VideoPanelWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Video Panel")
        self.resize(1200, 800)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.middle_panel = QWidget()
        self.setCentralWidget(self.middle_panel)

        middle_layout = QVBoxLayout(self.middle_panel)
        middle_layout.setContentsMargins(4, 4, 4, 0)
        middle_layout.setSpacing(0)
        self.middle_panel.setLayout(middle_layout)

        # Create a horizontal layout for label and button
        topbar_layout = QHBoxLayout()
        topbar_layout.setSpacing(0)

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

        topbar_layout.addWidget(self.label, 1)

        # Put a button to the right
        self.pop_in_button = PopInOutButton("popin")
        
        self.pop_in_button.clicked.connect(self.pop_in_panel)
        middle_layout.addWidget(self.pop_in_button, 0, Qt.AlignRight)
        topbar_layout.addWidget(self.pop_in_button, 0, Qt.AlignRight)


        # Add the horizontal layout to the middle layout
        middle_layout.addLayout(topbar_layout)

    def set_content(self, content_widget):
        self.middle_panel.layout().insertWidget(1, content_widget)  # Add content below the frame

    def clear_content(self):
        while self.middle_panel.layout().count() > 1:
            item = self.middle_panel.layout().takeAt(1)
            if item.widget():
                item.widget().setParent(None)

    def pop_in_panel(self):
        self.main_window.pop_in_panel()


class ImageViewer(QGraphicsView):
    
    '''Just placeholder for fun, until figuring out how the hell Rope handles video....'''
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self._zoom = 0
        self._empty = True
        self.image = None
        self._panning = False
        self._pan_start = QPointF()
        self.zoom_enabled = False  # Boolean to control zooming and panning

        self.setStyleSheet(styles.video_viewer)


    # Handling all the events for zooming and panning the image
    def setImage(self, image_path):
        image = QImage(image_path)
        if image.isNull():
            return
        self.scene.clear()
        self.image = QPixmap.fromImage(image)
        self.scene.addPixmap(self.image)
        self.setSceneRect(QRectF(self.image.rect()))
        self._empty = False
        if not self.zoom_enabled:
            self.fitToWindow()
    
    def getImage(self, image_path):
        return image_path

    def fitToWindow(self):
        if not self._empty:
            rect = self.viewport().rect()
            scene_rect = self.sceneRect()
            self.resetTransform()
            factor = min(rect.width() / scene_rect.width(), rect.height() / scene_rect.height())
            self.scale(factor, factor)

    def resizeEvent(self, event):
        if not self.zoom_enabled and not self._empty:
            self.fitToWindow()
        super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        if not self.zoom_enabled or self._empty:
            return
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    def mousePressEvent(self, event: QMouseEvent):
        if self.zoom_enabled and event.button() == Qt.MiddleButton:
            self._panning = True
            self._pan_start = event.position()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.zoom_enabled and self._panning:
            delta = event.position() - self._pan_start
            self._pan_start = event.position()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.zoom_enabled and event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def toggleZoom(self, button):
        self.zoom_enabled = not self.zoom_enabled
        if not self.zoom_enabled:
            self.fitToWindow()
            button.setText("Zoom Mode")
            button.setIcon(gui.get_icon("zoom"))
        else:
            self.resetTransform()
            button.setText("Aspect Mode")
            button.setIcon(gui.get_icon("aspect"))


class PlayerButton(QPushButton):
    def __init__(self, parent=None, icon="", icon_x=20, icon_y=20):
        super().__init__()
        self.setIcon(gui.get_icon(icon))
        self.setIconSize(QSize(icon_x, icon_y))
        self.setStyleSheet("""        
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
        """)
        
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(20, 20)
        parent.addWidget(self)


class PopInOutButton(QPushButton):
    def __init__(self, icon, tooltip_text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIcon(gui.get_icon(icon))
        self.setToolTip("Pop the video panel in or out of the main interface")  # Set the tooltip text
        self.setStyleSheet("""
                           QPushButton { 
                                background-color: #0d0d0d; 
                                border-radius: 6px; border: 0px; padding: 2px;
                                border-top-left-radius: 0px; 
                                border-top-right-radius: 8px;
                                border-bottom-left-radius: 0px; 
                                border-bottom-right-radius: 0px;
                            }
                            QPushButton:hover {
                                background-color: #181818;
                            }
                            QPushButton:pressed {
                                background-color: #0d0d0d;
                            }
                            QToolTip {
                                color: #d3d3d3;
                                background-color: #1a1a1a;
                                border: 0px;
                                padding: 5px;
                            }
                            """)

        self.setMinimumWidth(11)

