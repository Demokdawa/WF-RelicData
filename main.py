from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from part_detector import UIMainWindow


class MainWindow(QtWidgets.QMainWindow, UIMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupui(self)
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
