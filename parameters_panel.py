from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QPoint, Property, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QPainterPath, QColor, QIntValidator
import styles as styles


  
# ----------------------------- Main Parameters Panel -----------------------------
  
class ParametersSidePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__()  # Initialize without parent to avoid errors
        self.setContentsMargins(0, 4, 4, 4)
        main_width = 280
        # Scrollable area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setMinimumWidth(main_width) 
        scroll_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(styles.scroll_area)

        # Content widget inside the scroll area
        content_widget = QWidget()
        content_widget.setContentsMargins(4, 0, 4, 0)
        content_widget.setStyleSheet("QWidget { background-color: transparent; }")

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(4, 10, 4, 4)
        content_layout.setSpacing(5)
        content_layout.setAlignment(Qt.AlignTop)


        # Parameters and their panels
        restorer_panel = RestorerParameters(content_layout)
        restorer_toggle_label = ToggleWithLabel(content_layout, "Restorer", toggle_callback, toggle_panel=restorer_panel)
        content_layout.addWidget(restorer_toggle_label)
        content_layout.addWidget(restorer_panel)
        
        orientation_panel = RestorerParameters(content_layout)
        orientation_toggle_label = ToggleWithLabel(content_layout, "Orientation", toggle_callback, toggle_panel=orientation_panel)
        content_layout.addWidget(orientation_toggle_label)
        content_layout.addWidget(orientation_panel)
        
        strength_panel = RestorerParameters(content_layout)
        strength_toggle_label = ToggleWithLabel(content_layout, "Strength", toggle_callback, toggle_panel=strength_panel)
        content_layout.addWidget(strength_toggle_label)
        content_layout.addWidget(strength_panel)

        # Set the content widget as the widget of the scroll area
        scroll_area.setWidget(content_widget)
        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)
        # Ensure the parent is a layout and add the ParametersPanel to it
        parent.addWidget(self)




class RestorerParameters(QWidget):
    def __init__(self, parent=None):
        super().__init__()  # Initialize without parent to avoid errors
        # Restorer Parameters Panel
        
        self.setContentsMargins(0, 0, 0, 0)
        # self.setFixedHeight(50)
        self.setStyleSheet("QWidget { background-color: #191919; border-radius: 8px;}")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(3)
        # layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        
        ########### Slider Template
        slider = SliderWithEntry(parent_layout=layout, label_text="Slider", slider_range=(0, 100), initial_value=0, callback=slider_callback)


        ########### Dropdown Template
        widget5 = QWidget()
        widget5.setContentsMargins(0, 0, 0, 0)
        
        widget5.setStyleSheet("QWidget { background-color:transparent; border-radius: 0px;}")
        slider5_label_layout = QHBoxLayout()
        slider5_label_layout.setContentsMargins(0, 0, 0, 0)
        
        slider5_label = QLabel("Sider with big name")
        slider5 = DropdownExample(options=["1st Option", "2nd Option", "3rd Option", "4th Option"], default="2nd Option", callback=dropdown_callback)
        slider5.setFixedWidth(130)
        slider5_label_layout.addWidget(slider5_label)
        slider5_label_layout.addWidget(slider5)
        widget5.setLayout(slider5_label_layout)
        layout.addWidget(widget5)
        





# ----------------------------- UI Elements -----------------------------
        

        self.setVisible(False) 
    

class SliderWithEntry(QWidget):
    class CustomLineEdit(QLineEdit):
        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.clearFocus()
            else:
                super().keyPressEvent(event)

    def __init__(self, parent_layout = None, label_text="Slider", slider_range=(0, 100), initial_value=0, callback=None, parent=None):
        super().__init__(parent)
        self.callback = callback

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("QWidget { background-color:transparent; border-radius: 0px;}")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFixedWidth(120)
        self.slider.setRange(slider_range[0], slider_range[1])
        self.slider.setValue(initial_value)
        self.slider.setStyleSheet(styles.slider)  # Replace with your style

        self.entry = self.CustomLineEdit()
        self.entry.setStyleSheet("QLineEdit { background-color: #262626; color: #7d7d7d; border: none; border-radius: 4px; padding: 2px; }")
        self.entry.setFixedWidth(25)
        self.entry.setFixedHeight(15)
        self.entry.setValidator(QIntValidator(slider_range[0], slider_range[1]))  # Accept only integers within the slider range
        self.entry.setText(str(self.slider.value()))

        # Connect slider value changes to QLineEdit
        self.slider.valueChanged.connect(self.slider_value_changed)

        # Connect QLineEdit changes to slider value
        self.entry.textChanged.connect(self.entry_value_changed)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.entry)

        parent_layout.addWidget(self)
        
    def slider_value_changed(self, value):
        self.entry.setText(str(value))
        if self.callback:
            self.callback(value)

    def entry_value_changed(self, text):
        self.slider.setValue(int(text) if text.isdigit() else 0)
        if self.callback:
            self.callback(int(text) if text.isdigit() else 0)


        
# A whole goddamn custom dropdown made from scratch because the default combobox has this stupid problem
# https://stackoverflow.com/questions/27962162/rounded-qcombobox-without-square-box-behind 


class DropdownExample(QWidget):
    def __init__(self, options=None, default="Select an option", callback=None):
        super().__init__()

        if default not in options:
            raise ValueError(f"Default option '{default}' is not in the options list")

        self.setStyleSheet("background-color: #1e1e1e; color: white; border-radius: 4px;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton(default) 
        self.button.clicked.connect(self.show_menu)

        layout.addWidget(self.button)

        self.dropdown = CustomDropdown(self, width=self.button.width(), options=options, callback=callback)
        self.dropdown.set_default_option(default)  # Set the default option

    def show_menu(self):
        button_rect = self.button.rect()
        button_pos = self.button.mapToGlobal(button_rect.bottomLeft())
        self.dropdown.setFixedWidth(self.button.width())
        self.dropdown.show_at(button_pos)

    def get_current_option(self):
        return self.button.text()

def test_callback(selected_option):
    print(f"Selected option: {selected_option}")
    

class CustomDropdown(QWidget):
    def __init__(self, parent=None, width=200, options=None, callback=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(width)
        self.setMouseTracking(True)
        self.callback = callback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.options = []
        if options is None:
            options = [f"Option {i}" for i in range(1, 5)]

        for option in options:
            label = HoverLabel(option, self)
            label.setMouseTracking(True)
            label.setFixedHeight(20)
            label.mousePressEvent = lambda event, text=option: self.option_selected(event, text)
            layout.addWidget(label)
            self.options.append(label)

    def option_selected(self, event, text):
        self.parent().button.setText(text)
        self.hide()
        if self.callback:
            self.callback(text)

    def set_default_option(self, text):
        self.parent().button.setText(text)

    def show_at(self, pos):
        self.move(pos)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(rect, 8, 8)
        painter.fillPath(path, QColor("#2a2a2a"))  # Dropdown bg color
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

    def mouseMoveEvent(self, event):
        pos = event.pos()

        for label in self.options:
            if label.geometry().contains(pos):
                label.set_hover()
            else:
                label.set_default()

        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        for label in self.options:
            label.set_default()
        super().leaveEvent(event)
        

class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
        else:
            super().keyPressEvent(event)

class HoverLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.default_color = "#3c3c3c"
        self.hover_color = "#343434"
        self.set_default()
        self.setMouseTracking(True)
        self.adjust_font()

    def adjust_font(self):
        font = self.font()
        font.setPointSize(8)  # Adjust the font size as needed to fit the smaller height
        self.setFont(font)

    def set_default(self):
        self.setStyleSheet(f"""
            QLabel {{
                padding: 0px 5px;  /* Adjust padding to fit the smaller height */
                color: #989898;
                background-color: #2a2a2a;
                border-radius: 4px;
            }}
        """)

    def set_hover(self):
        self.setStyleSheet(f"""
            QLabel {{
                padding: 0px 5px;  /* Adjust padding to fit the smaller height */
                color: white;
                background-color: #323232;  /* Dropdown bg color */
                border-radius: 4px;
            }}
        """)


class ToggleWithLabel(QWidget):
    def __init__(self, parent=None, label=None, callback=None, toggle_panel=None, ):
        super().__init__()  # Initialize without parent to avoid errors
        self.toggle_panel = toggle_panel
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        self.label = QLabel(label)
        self.toggle = Toggle(bg_color="#4d4d4d", circle_color="#171717", active_color="#74db19", callback=callback)
        layout.addWidget(self.toggle)
        layout.addWidget(self.label)
        self.toggle.stateChanged.connect(self.on_toggle_state_changed)
        # parent.addWidget(self)
        
    def on_toggle_state_changed(self, state):
        if self.toggle_panel:
            self.toggle_panel.setVisible(self.toggle.isChecked())



class Toggle(QCheckBox):
    def __init__(self, 
                 bg_color="#000000", 
                 circle_color="#000000", 
                 active_color="#000000",  
                 callback=None, 
                 *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        width = 25
        height = 12
        
        self.animation_curve = QEasingCurve.Linear
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color
        self._circle_position = 1
        self.callback = callback

        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(self.animation_curve)
        self.animation.setDuration(100)
        
        self.stateChanged.connect(self.start_transition)

        
    @Property(float)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
        
    def start_transition(self, value):
        if self.callback:
            self.callback(value, self.isChecked())
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() + 1 - self.height())
        else:
            self.animation.setEndValue(1)
        self.animation.start()
        
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
        
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        
        rect = QRect(0, 0, self.width(), self.height())
        
        if self.isChecked():
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
            
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 1, 10, 10)

        else:
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
            
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 1, 10, 10)
        
        p.end()
        

#Test Callback
def toggle_callback(state, is_checked):
    print(f"{is_checked}")

def dropdown_callback(selected_option):
    print(f"Selected option: {selected_option}")


def slider_callback(value):
    print(f"Current value: {value}")
  