
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
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFileDialog, QMainWindow, QLabel, QWidget, QVBoxLayout, QGridLayout, QPushButton, QAction, QSizePolicy, QSlider, QStyle


## Create a subclasses of QMainWindow to setup the GUI
# camera window
class CameraWindow(QWidget):
    
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

        #create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        #create button for playing
        #self.playBtn = QPushButton()
        #self.playBtn.setEnabled(False)
        #self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        #self.playBtn.clicked.connect(self.play_video)

        #create slider
        #self.slider = QSlider(Qt.Horizontal)
        #self.slider.setRange(0,0)
        #self.slider.sliderMoved.connect(self.set_position)

        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create close button
        closeBtn = QPushButton('quit')
        closeBtn.clicked.connect(self.close)
        
        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(closeBtn)
        #hboxLayout.addWidget(self.playBtn)
        #hboxLayout.addWidget(self.slider)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)
        #media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        #self.mediaPlayer.positionChanged.connect(self.position_changed)
        #self.mediaPlayer.durationChanged.connect(self.duration_changed)


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()


    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    #def position_changed(self, position):
    #    self.slider.setValue(position)


    #def duration_changed(self, duration):
    #    self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
        

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