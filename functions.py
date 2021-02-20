# Filename: functions.py

__version__ = '0.1'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import subprocess

## App launcher functions ##############################
# Navit
def startNavit():
    app = '/usr/bin/navit'
    subprocess.Popen([app])
    
# Reverse camera / execute a terminal command with subprocess
def startCam():
    # -fs -> fullscreen
    # tv: -> source path
    subprocess.run(['mplayer', '-fs', 'tv:///dev/video0'])