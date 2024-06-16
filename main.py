from PySide6.QtWidgets import QApplication
import gui as gui



if __name__ == "__main__":
    app = QApplication([])

    main = gui.MainWindow()
    window = main
    window.show()
    
    app.exec()