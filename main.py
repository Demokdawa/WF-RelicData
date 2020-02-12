from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QSystemTrayIcon, QMenu, QAction
from pynput import keyboard
from os import path
import sys
import time
import threading
import grpc
import relic_pb2
import relic_pb2_grpc
import pyautogui
import pytesseract
import cv2
import numpy as np
import sqlite3
import unidecode

grpc_connect = '195.154.173.75:50051'

basepath = path.dirname(__file__)
tessdata_path = basepath + '/tessdata'
language = 'FR'
file = 'ref_fr.txt'

busy = False

pos_list = [(483, 411, 709, 458), (725, 411, 951, 458), (968, 411, 1193, 458), (1211, 411, 1436, 458)]

def parse_language():
    if language == 'FR':
        ref_language = {}
        with open(file, "r", encoding='utf8') as fileHandler:
            for line in fileHandler:
                ref_language[unidecode.unidecode(line.split(",")[1]).rstrip()] = unidecode.unidecode(line.split(",")[0]).rstrip()
        return ref_language
    else:
        pass

# Image processing for better detection after
def create_mask(theme, img):
    if theme == 'Virtuvian':
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_virtu = np.array([-3, 80, 80])
        upper_virtu = np.array([43, 255, 255])
        mask = cv2.inRange(hsv, lower_virtu, upper_virtu)
        return mask
    if theme == 'Stalker':
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_stalk = np.array([159, 80, 80])
        upper_stalk = np.array([199, 255, 255])
        mask = cv2.inRange(hsv, lower_stalk, upper_stalk)
        return mask
    if theme == 'Ancient':
        return img
    if theme == 'Equinox':
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_equi = np.array([107, 0, 0])
        upper_equi = np.array([127, 255, 255])
        mask = cv2.inRange(hsv, lower_equi, upper_equi)
        return mask
    if theme == 'Fortuna':
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_equi = np.array([80, 80, 84])
        upper_equi = np.array([120, 199, 255])
        mask = cv2.inRange(hsv, lower_equi, upper_equi)
        return mask
        

# Crop an area of a relic
def relicarea_crop(upper_y, downer_y, left_x, right_x, img):
    # upperY:downerY, LeftX:RightX
    cropped = img[upper_y:downer_y, left_x:right_x]
    return cropped
    

# Get Ducats/Plat values from DB
def get_data_from_db(prime_part):
    db = sqlite3.connect('data.sqlite3')
    cursor = db.cursor()
    cursor.execute('''SELECT PricePlat, PriceDucats FROM PrimePartData WHERE Name = ?''', (prime_part,))
    result_db = cursor.fetchone()
    return result_db
    

def normalize_names(name):
    dict_test = parse_language()
    test1 = name.replace('\n', ' ')
    test2 = dict_test.get(unidecode.unidecode(test1).upper())
    test3 = test2.title()
    return test3

def data_pass_name(pos1, pos2, pos3, pos4, image):
    img_file = 'theme_source.png'
    image = cv2.imread(img_file)
    cropped_img = relicarea_crop(pos1, pos2, pos3, pos4, image)
    upscaled = cv2.resize(cropped_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    ret, imgtresh = cv2.threshold(create_mask('Virtuvian', upscaled), 218, 255, cv2.THRESH_BINARY_INV)
    tessdata_dir_config = '--tessdata-dir "C:/Users/aprieto/Documents/GitHub/WF-RelicData/tessdata" -l Roboto --oem 1 --psm 6 get.images'
    textocr = pytesseract.image_to_string(imgtresh, config=tessdata_dir_config)
    return textocr
    
    
def recognize():
    opencvImage = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    rel_values = []
    for i in pos_list:
        result = data_pass_name(i[1], i[3], i[0], i[2], opencvImage)
        plats, ducats = get_data_from_db(normalize_names(result))
        rel_values.append((plats, ducats, i[0], i[1]))
    return rel_values


def get_serv_data():
    channel = grpc.insecure_channel(grpc_connect)
    stub = relic_pb2_grpc.DataSenderStub(channel)
    response = stub.send_data(relic_pb2.Empty())
    serv_data = bytes(response.data)
    open('data.sqlite3', 'wb').write(serv_data)
    
    
def on_press(key):
    try:
        pass
        # print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        pass

def execute_things():
    global busy
    print('execute ' + busy)
    princ.hide()
    busy = False
    print('triggered')

def on_release(key):
    global busy
    print('First ' + busy)
    # print('{0} released'.format(key))
    if busy is False and key == keyboard.Key.f12:
        busy = True
        princ.update_vals(recognize())
        princ.show()
        timer = threading.Timer(5, execute_things)
        timer.start()
    if busy is True and key == keyboard.Key.f12:
        print('false ' + busy)


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
            QtCore.Qt.X11BypassWindowManagerHint |
            QtCore.Qt.Tool
                            )
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        
        # Tray Menu Part
        self.icon = QtGui.QIcon("icon.png")

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.menu = QMenu()
        
        self.action = QAction("RelicScanner prêt !")
        self.action.setFont(QtGui.QFont('Aharoni', 12, weight=QtGui.QFont.Bold))
        self.menu.addAction(self.action)
        self.action.setEnabled(False)
        
        self.exitAction = QAction("&Exit")
        self.menu.addAction(self.exitAction)
        self.exitAction.triggered.connect(exit)
        
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        
        # Element 1
        self.img_ducat_1 = QLabel(self)
        self.img_ducat_1.setPixmap(QtGui.QPixmap("ducat.png"))
        self.img_ducat_1.move(453, 230)
        self.img_plat_1 = QLabel(self)
        self.img_plat_1.setPixmap(QtGui.QPixmap("plat.png"))
        self.img_plat_1.move(453, 265)
        self.label_ducat_1 = QLabel('X', self)
        self.label_ducat_1.move(483, 230)
        self.label_ducat_1.setFont(QtGui.QFont('Impact', 14))
        self.label_plat_1 = QLabel('X', self)
        self.label_plat_1.move(483, 265)
        self.label_plat_1.setFont(QtGui.QFont('Impact', 14))

        # Element 2
        self.img_ducat_2 = QLabel(self)
        self.img_ducat_2.setPixmap(QtGui.QPixmap("ducat.png"))
        self.img_ducat_2.move(695, 230)
        self.img_plat_2 = QLabel(self)
        self.img_plat_2.setPixmap(QtGui.QPixmap("plat.png"))
        self.img_plat_2.move(695, 265)
        self.label_ducat_2 = QLabel('X', self)
        self.label_ducat_2.move(725, 230)
        self.label_ducat_2.setFont(QtGui.QFont('Impact', 14))
        self.label_plat_2 = QLabel('X', self)
        self.label_plat_2.move(725, 265)
        self.label_plat_2.setFont(QtGui.QFont('Impact', 14))

        # Element 3
        self.img_ducat_3 = QLabel(self)
        self.img_ducat_3.setPixmap(QtGui.QPixmap("ducat.png"))
        self.img_ducat_3.move(938, 230)
        self.img_plat_3 = QLabel(self)
        self.img_plat_3.setPixmap(QtGui.QPixmap("plat.png"))
        self.img_plat_3.move(938, 265)
        self.label_ducat_3 = QLabel('X', self)
        self.label_ducat_3.move(968, 230)
        self.label_ducat_3.setFont(QtGui.QFont('Impact', 14))
        self.label_plat_3 = QLabel('X', self)
        self.label_plat_3.move(968, 265)
        self.label_plat_3.setFont(QtGui.QFont('Impact', 14))

        # Element 4
        self.img_ducat_4 = QLabel(self)
        self.img_ducat_4.setPixmap(QtGui.QPixmap("ducat.png"))
        self.img_ducat_4.move(1181, 230)
        self.img_plat_4 = QLabel(self)
        self.img_plat_4.setPixmap(QtGui.QPixmap("plat.png"))
        self.img_plat_4.move(1181, 265)
        self.label_ducat_4 = QLabel('X', self)
        self.label_ducat_4.move(1211, 230)
        self.label_ducat_4.setFont(QtGui.QFont('Impact', 14))
        self.label_plat_4 = QLabel('X', self)
        self.label_plat_4.move(1211, 265)
        self.label_plat_4.setFont(QtGui.QFont('Impact', 14))
       
        
    def update_vals(self, data):
        self.label_ducat_1.setText(str(data[0][1]))
        self.label_plat_1.setText(str(data[0][0]))
        self.label_ducat_2.setText(str(data[1][1]))
        self.label_plat_2.setText(str(data[1][0]))
        self.label_ducat_3.setText(str(data[2][1]))
        self.label_plat_3.setText(str(data[2][0]))
        self.label_ducat_4.setText(str(data[3][1]))
        self.label_plat_4.setText(str(data[3][0]))

if __name__ == '__main__':
    get_serv_data()
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    princ = Fenetre()
    sys.exit(app.exec_())

