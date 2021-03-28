
# Filename: ui.py

__version__ = '0.1'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import sys
#import mpylayer
# import styles
import style
import functions
import cv2

# PyQt5 packages
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QTimer, Qt, QRect, QCoreApplication, QMetaObject, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QDialog, QMainWindow, QLabel, QWidget, QVBoxLayout, QGridLayout, QPushButton, QSizePolicy

#######################################################################
class VideoStream(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(
                    FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(480, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.wait()

#######################################################################
class CameraWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('camera')
        #self.setFixedSize(635, 635)  # use variables
        self.showFullScreen()

        self.image_label = QLabel(self)
        self.image_label.showFullScreen()
        #self.image_label.resize(580, 580)


        cLayout = QVBoxLayout()
        cLayout.addWidget(self.image_label, 0)
        camera_quit = QPushButton('quit camera')
        cLayout.addWidget(camera_quit, 1)
        camera_quit.clicked.connect(self.CancelFeed)
        camera_quit.clicked.connect(self.close)

        self.setLayout(cLayout)

        self.thread = VideoStream()
        self.thread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.thread.start()

    def ImageUpdateSlot(self, Image):
        self.image_label.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.thread.stop()
    
        
#######################################################################
class Navigator(QMainWindow):

    def _createButtons(self):
        
        # Navit
        btn_navit = QPushButton()
        btn_navit.setStyleSheet(style.btn_navit) # -> to style variable style.btn_navit
        btn_navit.clicked.connect(functions.startNavit)
        
        # Camera
        btn_camera = QPushButton()
        btn_camera.setStyleSheet(style.btn_camera) # -> to style variable style.btn_camera
        btn_camera.clicked.connect(self.camera_window)
        
        # Sensors
        btn_sensors = QPushButton()
        btn_sensors.setStyleSheet(style.btn_sensors) # -> to style variable style.btn_sensors
       
        # Quit
        btn_quit = QPushButton()
        btn_quit.setStyleSheet(style.btn_quit) # -> to style variable style.btn_quit
        btn_quit.clicked.connect(self.close)
        
        # Add buttonsLayout to the general layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(btn_navit, 1, 0)
        mainLayout.addWidget(btn_camera, 1, 1)
        mainLayout.addWidget(btn_sensors, 1, 2)
        mainLayout.addWidget(btn_quit, 2, 0, 2, 3) # (row, column, rows, columns)

        self.generalLayout.addLayout(mainLayout)

    ## root window
    def __init__(self):
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Navigator')
        #self.setFixedSize(635, 635)
        self.showFullScreen()
        self.setStyleSheet(style.mainWindow) # -> to style variable style.mainWindow
        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        #self._createDisplay()
        self._createButtons()

    def camera_window(self, checked):
        self.w = CameraWindow()
        self.w.show()
        
#######################################################################
def main():
    # Create an instance of QApplication
    navigator = QApplication(sys.argv)
    view = Navigator()
    view.show()
    sys.exit(navigator.exec_())

if __name__ == '__main__':
    main()


### NOTES: split files into Functions, Styles. Gorup layouts by window