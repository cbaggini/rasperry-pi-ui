
# Filename: ui.py

__version__ = '0.1'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QGridLayout, QPushButton
# import styles
import style
import functions


## Create a subclasses of QMainWindow to setup the GUI
# camera window
class CameraWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        
        self.label = QLabel('Camera Window')
        self.button = QPushButton('quit')
        self.button.clicked.connect(self.close)
        self.setFixedSize(635, 635)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        



# Main window
class Navigator(QMainWindow):

    def _createButtons(self):
        ## Buttons ############################################
        mainLayout = QGridLayout()
        # Navit
        btn_navit = QPushButton()
        btn_navit.setStyleSheet(style.btn_navit) # -> to style variable style.btn_navit
        btn_navit.clicked.connect(functions.startNavit)
        mainLayout.addWidget(btn_navit, 1, 0)

        # Camera
        btn_camera = QPushButton()
        btn_camera.setStyleSheet(style.btn_camera) # -> to style variable style.btn_camera
        btn_camera.clicked.connect(functions.startCam)
        mainLayout.addWidget(btn_camera, 1, 1)

        # Sensors
        btn_sensors = QPushButton()
        btn_sensors.setStyleSheet(style.btn_sensors) # -> to style variable style.btn_sensors
        mainLayout.addWidget(btn_sensors, 1, 2)

        # Quit
        btn_quit = QPushButton()
        btn_quit.setStyleSheet(style.btn_quit) # -> to style variable style.btn_quit
        btn_quit.clicked.connect(self.close)
        mainLayout.addWidget(btn_quit, 2, 0, 2, 3)

        btn_new = QPushButton('Camera window')
        #btn_new.setStyleSheet(style.btn_quit) # -> to style variable style.btn_quit
        btn_new.clicked.connect(self.camera_window)
        mainLayout.addWidget(btn_new, 3, 0, 2, 3)

        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(mainLayout)


    ## root window
    def __init__(self):
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Navigator')
        self.setFixedSize(635, 635)
        self.setStyleSheet(style.mainWindow) # -> to style variable style.mainWindow
        # self.showFullScreen()
        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        # self._createDisplay()
        self._createButtons()

    def camera_window(self, checked):
            self.w = CameraWindow()
            self.w.show()

        

# Client code
def main():
    # Create an instance of QApplication
    navigator = QApplication(sys.argv)
    view = Navigator()
    view.show()
    sys.exit(navigator.exec_())

if __name__ == '__main__':
    main()


### NOTES: split files into Functions, Styles. Gorup layouts by window