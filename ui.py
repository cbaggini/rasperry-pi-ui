
# Filename: ui.py

__version__ = '0.1'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import sys
#import mpylayer
# import styles
import style
import functions

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
from threading import Thread, Lock
import time
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFileDialog, QMainWindow, QLabel, QWidget, QVBoxLayout, QGridLayout, QPushButton, QAction, QSizePolicy, QSlider, QStyle


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(972, 667)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 630, 451, 28))
        self.pushButton.setObjectName("pushButton")
        #self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        #self.pushButton_2.setGeometry(QtCore.QRect(500, 630, 451, 28))
        #self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(24, 19, 931, 591))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Start Stream"))
        #self.pushButton_2.setText(_translate("Dialog", "Record"))

# ------------

class WebcamVideoStream :
    def __init__(self, src, width = 640, height = 480) :
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 5)
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self) :
        if self.started :
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self) :
        while self.started :
            (grabbed, frame) = self.stream.read()
            time.sleep(self.FPS)
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self) :
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self) :
        self.started = False
        if self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()

## Create a subclasses of QMainWindow to setup the GUI
# camera window
class CameraWindow(QtWidgets.QDialog, Ui_Dialog):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle('camera')
        self.setFixedSize(635, 635)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        self.init_ui()
        self.show()

    def init_ui(self):

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #create videowidget object
        videowidget = QVideoWidget()

        
        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create close button
        closeBtn = QPushButton('quit')
        closeBtn.clicked.connect(self.close)

        openBtn = QPushButton('open')
        openBtn.clicked.connect(self.start_cam)
        
        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(closeBtn)
        
        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)
        #media player signals

    def start_cam(self):
        self.capture = WebcamVideoStream(src = 0).start()
        self.timer=QTimer(self)
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(2)

    def update_frame(self):
        self.image=self.capture.read()
        self.displayImage(self.image)

    def displayImage(self,img):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        outImage=outImage.rgbSwapped()

        self.label.setPixmap(QPixmap.fromImage(outImage))
        self.label.setScaledContents(True)
        return outImage
        



        

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