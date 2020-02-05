import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel


class MainWindow(QMainWindow):
    def __init__(self, plats):
        QMainWindow.__init__(self)
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1080
        self.plats = plats
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
                            )
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        label = QLabel('yes', self)
        label.move(483, 411)

        label2 = QLabel('yes', self)
        label2.move(725, 411)

        label3 = QLabel('yes', self)
        label3.move(968, 411)

        label4 = QLabel('yes', self)
        label4.move(1211, 411)


def show_overlay():
    app = QApplication(sys.argv)
    mywindow = MainWindow('tamer')
    mywindow.show()
    app.exec_()

show_overlay()
