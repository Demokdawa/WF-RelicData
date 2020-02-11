import pytesseract
import cv2
import numpy as np
import shutil
from os import path
import sqlite3
import unidecode
from pynput import keyboard
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import sys
import time

basepath = path.dirname(__file__)
tessdata_path = basepath + '/tessdata'
language = 'FR'
file = basepath + '/ref_fr.txt'

pos_list = [(483, 411, 709, 458), (725, 411, 951, 458), (968, 411, 1193, 458), (1211, 411, 1436, 458)]


def parse_language():
    if language == 'FR':
        ref_language = {}
        with open(file, "r", encoding='utf8') as fileHandler:
            for line in fileHandler:
                ref_language[unidecode.unidecode(line.split(",")[1]).rstrip()] = unidecode.unidecode(line.split(",")[0]).rstrip()
        print(ref_language)
        return ref_language
    else:
        pass


dict_test = parse_language()


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
    db = sqlite3.connect('relicdb.sqlite3')
    cursor = db.cursor()
    cursor.execute('''SELECT PricePlat, PriceDucats FROM PrimePartData WHERE Name = ?''', (prime_part,))
    result_db = cursor.fetchone()
    return result_db


def normalize_names(name):
    test1 = name.replace('\n', ' ')
    test2 = dict_test.get(unidecode.unidecode(test1).upper())
    test3 = test2.title()
    return test3


def data_pass_name(pos1, pos2, pos3, pos4):
    img_file = 'theme_source.png'
    image = cv2.imread(img_file)
    cropped_img = relicarea_crop(pos1, pos2, pos3, pos4, image)
    upscaled = cv2.resize(cropped_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # cv2.imwrite(basepath + 'raw.jpg', upscaled)
    ret, imgtresh = cv2.threshold(create_mask('Virtuvian', upscaled), 218, 255, cv2.THRESH_BINARY_INV)
    # cv2.imwrite(basepath + '/mask.jpg', create_mask('Virtuvian', upscaled))
    # cv2.imwrite(basepath + '/after-mask.jpg', imgtresh)
    tessdata_dir_config = '--tessdata-dir "C:/Users/Demokdawa/PycharmProjects/WF-RelicData/tessdata" -l Roboto --oem 1 --psm 6 get.images'
    textocr = pytesseract.image_to_string(imgtresh, config=tessdata_dir_config)
    # tiffname = basepath + '/test.tif'
    # shutil.move(basepath + '/tessinput.tif', tiffname)
    return textocr


def recognize():
    rel_values = []
    for i in pos_list:
        result = data_pass_name(i[1], i[3], i[0], i[2])
        print(normalize_names(result))
        plats, ducats = get_data_from_db(normalize_names(result))
        rel_values.append((plats, ducats, i[0], i[1]))
    return rel_values


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
        data = recognize()
        show_overlay()
    elif key == keyboard.Key.esc:
        # Stop listener
        return False


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
    time.sleep(10)
    mywindow.close()
    app.exec_()

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

show_overlay()
