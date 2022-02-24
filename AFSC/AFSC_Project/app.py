### System

import sys
import shutil
import os
import time
import socket
from subprocess import Popen, PIPE, STDOUT, call
import threading

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

### Interfaces
from mainwindow import MainWindow


app = qtw.QApplication(sys.argv)
app.setApplicationName("Virtual Machine Forensic Tool")
widget = qtw.QStackedWidget()
main = MainWindow(widget)
widget.addWidget(main)
widget.setFixedHeight(407)
widget.setFixedWidth(606)

widget.show()

try:

    sys.exit(app.exec_())
    
except:
    print("EXIT")
