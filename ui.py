
# Filename: ui.py

__version__ = '0.3'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import sys
import os
#import mpylayer
# import styles
import style
import functions
import cv2

# PyQt5 packages
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
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
                Pic = ConvertToQtFormat.scaled(1024, 512, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.wait()


#######################################################################
class MediaPlayer(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('media player')
        self.setFixedSize(1280, 720)  # use variables
        #self.showFullScreen()
        self.setStyleSheet(style.cameraWindow)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        mLayout = QVBoxLayout()
        
        mLayout.addWidget(self.image_label, 0)
        media_quit = QPushButton()
        media_quit.setStyleSheet(style.btn_back)
        mLayout.addWidget(media_quit, 1)
        media_quit.clicked.connect(self.close)

        self.setLayout(mLayout)


#######################################################################
class CameraWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('camera')
        self.setFixedSize(1280, 720)  # use variables
        #self.showFullScreen()
        self.setStyleSheet(style.cameraWindow)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cLayout = QVBoxLayout()
        
        cLayout.addWidget(self.image_label, 0)
        camera_quit = QPushButton()
        camera_quit.setStyleSheet(style.btn_back)
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
        btn_navit.setStyleSheet(style.btn_navit)
        btn_navit.clicked.connect(functions.startNavit)
        
        # Camera
        btn_camera = QPushButton()
        btn_camera.setStyleSheet(style.btn_camera)
        btn_camera.clicked.connect(self.camera_window)
        
        # Sensors
        btn_sensors = QPushButton()
        btn_sensors.setStyleSheet(style.btn_sensors)
        btn_sensors.clicked.connect(self.media_player)

        # Quit
        btn_quit = QPushButton()
        btn_quit.setStyleSheet(style.btn_quit)
        btn_quit.clicked.connect(self.close)
        
        # Add buttonsLayout to the general layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(btn_navit, 1, 0)
        mainLayout.addWidget(btn_camera, 1, 1)
        mainLayout.addWidget(btn_sensors, 1, 2)
        mainLayout.addWidget(btn_quit, 2, 0, 2, 3)

        self.generalLayout.addLayout(mainLayout)

    ## root window
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Navigator')
        self.setFixedSize(1280, 720)
        #self.showFullScreen()
        self.setStyleSheet(style.mainWindow)
        
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        #self._createDisplay()
        self._createButtons()

    def camera_window(self, checked):
        self.w = CameraWindow()
        self.w.show()

    def media_player(self, checked):
        self.m = MediaPlayer()
        self.m.show()

    def Poweroff(channel):
        os.system("sudo poweroff -h now")

        
#######################################################################
def main():
    
    navigator = QApplication(sys.argv)
    view = Navigator()
    view.show()
    sys.exit(navigator.exec_())

if __name__ == '__main__':
    main()


### NOTES: split files into Functions, Styles. Group layouts by window