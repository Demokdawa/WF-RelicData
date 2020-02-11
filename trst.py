import sys
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from pynput import keyboard
import time
import threading


def on_press(key):
    try:
        pass
        # print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        pass


def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.f11:
        princ.show()
        timer = threading.Timer(60, princ.hide)
        timer.start()
    elif key == keyboard.Key.esc:
        # Stop listener
        return False


class Fenetre(QtWidgets.QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1080
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
                            )
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        label = QLabel('yes', self)
        label.move(483, 411)

        label2 = QLabel('yes', self)
        label2.move(725, 411)

        label3 = QLabel('yes', self)
        label3.move(968, 411)

        label4 = QLabel('yes', self)
        label4.move(1211, 411)


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
app = QtWidgets.QApplication(sys.argv)
princ = Fenetre()
sys.exit(app.exec_())

