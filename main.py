from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QSystemTrayIcon, QMenu, QAction
from pynput import keyboard
from sys import argv,exit
import sys
import os
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
from random import randint
from pathlib import Path
from colour import Color
from spellchecker import SpellChecker

#INIT&VARS####################################################################################################

if getattr(sys, 'frozen', False):
    folder = Path(sys._MEIPASS)
else:
    folder = Path(__file__).parent
    
pytesseract.pytesseract.tesseract_cmd = os.path.join(str(folder), 'Tesseract-OCR', 'tesseract.exe')

tessdata_path = os.path.join(str(folder), 'tessdata')

grpc_connect = '195.154.173.75:50051'

language = 'FR'
file = os.path.join(str(folder), 'ref_fr.txt')

busy = False

pos_list = [(483, 411, 709, 458), (725, 411, 951, 458), (968, 411, 1193, 458), (1211, 411, 1436, 458)] #RES-DEPENDANT

##############################################################################################################
#UI-COLORS####################################################################################################

# RGB Format
ui_color_list_primary = [
    (190, 169, 102, 'Virtuvian'),             # Vitruvian
    (153,  31,  35, 'Stalker'),               # Stalker 
    (238, 193, 105, 'Baruk'),                 # Baruk
    ( 35, 201, 245, 'Corpus'),                # Corpus
    ( 57, 105, 192, 'Fortuna'),               # Fortuna
    (255, 189, 102, 'Grineer'),               # Grineer
    ( 36, 184, 242, 'Lotus'),                 # Lotus
    (140,  38,  92, 'Nidus'),                 # Nidus
    ( 20,  41,  29, 'Orokin'),                # Orokin
    (  9,  78, 106, 'Tenno'),                 # Tenno
    (  2, 127, 217, 'High contrast'),         # High contrast
    (255, 255, 255, 'Legacy'),                # Legacy
    (158, 159, 167, 'Equinox'),               # Equinox
    (140, 119, 147, 'Dark Lotus')             # Dark Lotus
]

ui_color_list_secondary = [
    (245, 227, 173, 'Virtuvian'),   
    (255,  61,  51, 'Stalker'),     
    (236, 211, 162, 'Baruk'),       
    (111, 229, 253, 'Corpus'),      
    (255, 115, 230, 'Fortuna'),     
    (255, 224, 153, 'Grineer'),     
    (255, 241, 191, 'Lotus'),           
    (245,  73,  93, 'Nidus'),           
    (178, 125,   5, 'Orokin'),  
    (  6, 106,  74, 'Tenno'),           
    (255, 255,   0, 'High contrast'),   
    (232, 213,  93, 'Legacy'),      
    (232, 227, 227, 'Equinox'), 
    (200, 169, 237, 'Dark Lotus')
]

# Check ui theme from screenshot (Image Format : OPENCV)
def get_theme(image, color_treshold):
    input_clr = image[86, 115] # Y,X  RES-DEPENDANT
    for e in ui_color_list:
        if abs(input_clr[2] - e[0]) < color_treshold and abs(input_clr[1] - e[1]) < color_treshold and abs(input_clr[0] - e[2]) < color_treshold:
            return e[3]
        else:
            pass
    
##############################################################################################################
#####TRESHOLD#################################################################################################


# Treshold Function
def get_treshold_2(image, theme):

    e_primary = [item for item in ui_color_list_primary if item[3] == theme][0]
    e_secondary = [item for item in ui_color_list_secondary if item[3] == theme][0]

    c_primary = Color(rgb=(e_primary[0] / 256, e_primary[1] / 256, e_primary[2] / 256))
    c_secondary = Color(rgb=(e_secondary[0] / 256, e_secondary[1] / 256, e_secondary[2] / 256))

    upscaled = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # Upscaling x2
    
    rgb_arr = image
    hsl_arr = cv2.cvtColor(upscaled, cv2.COLOR_BGR2HLS)  # Hue, Lighness, Saturation
    
    p_hue = round(c_primary.hue * 360) / 2
    p_hue_sec = round(c_secondary.hue * 360) / 2
    
    kernel = np.ones((3, 3), np.uint8)

    if theme == 'Virtuvian':  # WORKING
        method = 'HSL'
        HueOK = np.logical_and(hsl_arr[..., 0] > p_hue - 4 / 2, hsl_arr[..., 0] < p_hue + 4 / 2)
        SaturationOK = hsl_arr[..., 2] >= (0.25 * 256)
        LightnessOK = hsl_arr[..., 1] >= (0.42 * 256)
        combinedMask = HueOK & SaturationOK & LightnessOK
        
    elif theme == 'Stalker':  # WORKING
        method = 'HSL'
        HueOK = np.logical_and(hsl_arr[..., 0] > p_hue - 4 / 2, hsl_arr[..., 0] < p_hue + 4 / 2)
        SaturationOK = hsl_arr[..., 2] >= (0.5 * 256)
        LightnessOK = hsl_arr[..., 1] >= (0.20 * 256)
        combinedMask = HueOK & SaturationOK & LightnessOK
        
    elif theme == 'Baruk':
        pass
        
    elif theme == 'Corpus':
        pass
        
    elif theme == 'Fortuna':  # WORKING
        method = 'HSL'
        HueOK = np.logical_and(hsl_arr[..., 0] > p_hue - 4 / 2, hsl_arr[..., 0] < p_hue + 4 / 2)
        SaturationOK = hsl_arr[..., 2] >= (0.20 * 256)
        LightnessOK = hsl_arr[..., 1] >= (0.25 * 256)
        combinedMask = HueOK & SaturationOK & LightnessOK
        
    elif theme == 'Grineer':
        pass
        
    elif theme == 'Lotus':  # A TESTER
        method = 'HSL'
        HueOK = np.logical_and(hsl_arr[..., 0] > p_hue - 5 / 2, hsl_arr[..., 0] < p_hue + 5 / 2)
        SaturationOK = hsl_arr[..., 2] >= (0.65 * 256)
        LightnessOK = np.logical_and(hsl_arr[..., 1] >= p_lumi - 0.1, hsl_arr[..., 0] <= p_lumi + 0.1)
        # return Math.Abs(test.GetHue() - primary.GetHue()) < 5 & test.GetSaturation() >= 0.65 & & Math.Abs(
        #    test.GetBrightness() - primary.GetBrightness()) <= 0.1
        # | | (Math.Abs(test.GetHue() - secondary.GetHue()) < 4 & & test.GetBrightness() >= 0.65);
        combinedMask = HueOK & SaturationOK & LightnessOK
        
    elif theme == 'Nidus':
        method = 'BGR'
        lowerBound = np.array([(e_primary[2] - 40), (e_primary[1] - 40), (e_primary[0] - 40)])  # BGR
        upperBound = np.array([(e_primary[2] + 40), (e_primary[1] + 40), (e_primary[0] + 40)])  # BGR

    elif theme == 'Orokin':
        pass
        
    elif theme == 'Tenno':
        pass
        
    elif theme == 'High contrast':
        pass
        
    elif theme == 'Legacy':  # WORKS but NEED TESTING
        method = 'HSL'
        SaturationOK = hsl_arr[..., 2] <= (0.2 * 256)
        LightnessOK = hsl_arr[..., 1] >= (0.75 * 256)
        combinedMask = SaturationOK & LightnessOK
        pass
        
    elif theme == 'Equinox':  # WORKING
        method = 'HSL'
        HueOK = np.logical_and(hsl_arr[..., 0] > 110, hsl_arr[..., 0] < 135)
        SaturationOK = hsl_arr[..., 2] <= (0.1 * 255)
        LightnessOK = np.logical_and(hsl_arr[..., 1] >= (0.35 * 256), hsl_arr[..., 1] <= (0.74 * 256))
        combinedMask = HueOK & SaturationOK & LightnessOK

    elif theme == 'Dark Lotus':  # WORKING
        method = 'HSL'
        HueOK = np.logical_and(hsl_arr[..., 0] > 134, hsl_arr[..., 0] < 143)
        SaturationOK = np.logical_and(hsl_arr[..., 2] >= (0.11 * 256), hsl_arr[..., 2] <= (0.22 * 256))
        LightnessOK = np.logical_and(hsl_arr[..., 1] >= (0.43 * 256), hsl_arr[..., 2] <= (0.53 * 256))
        combinedMask = HueOK & SaturationOK & LightnessOK
    
    if method == 'BGR':
        filter = cv2.inRange(upscaled, lowerBound, upperBound)
        filered = cv2.bitwise_not(filter)
        tresh = cv2.erode(filered, kernel, iterations=1)
        
    elif method == 'HSL':
        hsl_arr[combinedMask] = 0
        hsl_arr[~combinedMask] = 255
        tresh = cv2.erode(hsl_arr, kernel, iterations=1)

    return tresh

##############################################################################################################



# Try to correct mistakes
def spell_correction_ocr(string, corr_list):
    spell_check_ocr = SpellChecker(distance=2, language=None, case_sensitive=False)
    spell_check_ocr.word_frequency.load_words(corr_list)
    spell_check_ocr.correction(string)
    return spell_check_ocr.correction(string).strip().capitalize()
    

def parse_language():
    if language == 'FR':
        ref_language = {}
        with open(file, "r", encoding='utf8') as fileHandler:
            for line in fileHandler:
                ref_language[unidecode.unidecode(line.split(",")[1]).rstrip()] = unidecode.unidecode(line.split(",")[0]).rstrip()
        return ref_language
    else:
        pass
        

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
    strip_newlines = name.replace('\n', ' ')
    translation = dict_test.get(unidecode.unidecode(strip_newlines).upper())
    if translation is None:
        return 'Bad'
    else:
        translation_format = translation.title()
        return translation_format

def data_pass_name(pos1, pos2, pos3, pos4, image2):
    img_file = str(folder) + '/test_ducat.png'
    image = cv2.imread(img_file)
    cropped_img = relicarea_crop(pos1, pos2, pos3, pos4, image)
    imgtresh_temp = get_treshold_2(cropped_img, 'Virtuvian')
    tessdata_dir_config = '--tessdata-dir "' + tessdata_path + '" -l Roboto --oem 1 --psm 6 get.images'
    textocr = pytesseract.image_to_string(imgtresh_temp, config=tessdata_dir_config)
    corrected = spell_correction_ocr(textocr, corr_list)
    print('ocr is : ' + textocr)
    return textocr
    
    
def recognize():
    opencvImage = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    rel_values = []
    for i in pos_list:
        result = data_pass_name(i[1], i[3], i[0], i[2], opencvImage)
        norm = normalize_names(result)
        print(norm)
        if norm == 'Bad':
            rel_values.append(('Bad', 'Bad', i[0], i[1]))
        else:
            plats, ducats = get_data_from_db(normalize_names(result))
            rel_values.append((plats, ducats, i[0], i[1]))
    return rel_values


def get_serv_data():
    channel = grpc.insecure_channel(grpc_connect)
    stub = relic_pb2_grpc.DataSenderStub(channel)
    response = stub.send_data(relic_pb2.Empty())
    serv_data = bytes(response.data)
    open('data.sqlite3', 'wb').write(serv_data)
 
#UI-Part################################################################################# 
    
def on_press(key):
    try:
        pass
        # print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        pass

def hide_UI():
    global busy
    princ.hide()
    busy = False

def on_release(key):
    global busy
    # print('{0} released'.format(key))
    if busy is False and key == keyboard.Key.f12:
        busy = True
        princ.update_vals(recognize())
        princ.show()
        timer = threading.Timer(5, hide_UI)
        timer.start()
    if busy is True and key == keyboard.Key.f12:
        pass


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
        self.icon = QtGui.QIcon(str(folder) + "/icon.png")

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
        self.img_ducat_1.setPixmap(QtGui.QPixmap(str(folder) + "/ducat.png"))
        self.img_ducat_1.move(453, 230)
        self.img_plat_1 = QLabel(self)
        self.img_plat_1.setPixmap(QtGui.QPixmap(str(folder) + "/plat.png"))
        self.img_plat_1.move(453, 265)
        self.label_ducat_1 = QLabel('X', self)
        self.label_ducat_1.move(483, 230)
        self.label_ducat_1.setFont(QtGui.QFont('Impact', 14))
        self.label_plat_1 = QLabel('X', self)
        self.label_plat_1.move(483, 265)
        self.label_plat_1.setFont(QtGui.QFont('Impact', 14))

        # Element 2
        self.img_ducat_2 = QLabel(self)
        self.img_ducat_2.setPixmap(QtGui.QPixmap(str(folder) + "/ducat.png"))
        self.img_ducat_2.move(695, 230)
        self.img_plat_2 = QLabel(self)
        self.img_plat_2.setPixmap(QtGui.QPixmap(str(folder) + "/plat.png"))
        self.img_plat_2.move(695, 265)
        self.label_ducat_2 = QLabel('X', self)
        self.label_ducat_2.move(725, 230)
        self.label_ducat_2.setFont(QtGui.QFont('Impact', 14))
        self.label_plat_2 = QLabel('X', self)
        self.label_plat_2.move(725, 265)
        self.label_plat_2.setFont(QtGui.QFont('Impact', 14))

        # Element 3
        self.img_ducat_3 = QLabel(self)
        self.img_ducat_3.setPixmap(QtGui.QPixmap(str(folder) + "/ducat.png"))
        self.img_ducat_3.move(938, 230)
        self.img_plat_3 = QLabel(self)
        self.img_plat_3.setPixmap(QtGui.QPixmap(str(folder) + "/plat.png"))
        self.img_plat_3.move(938, 265)
        self.label_ducat_3 = QLabel('X', self)
        self.label_ducat_3.move(968, 230)
        self.label_ducat_3.setFont(QtGui.QFont('Impact', 14))
        self.label_plat_3 = QLabel('X', self)
        self.label_plat_3.move(968, 265)
        self.label_plat_3.setFont(QtGui.QFont('Impact', 14))

        # Element 4
        self.img_ducat_4 = QLabel(self)
        self.img_ducat_4.setPixmap(QtGui.QPixmap(str(folder) + "/ducat.png"))
        self.img_ducat_4.move(1181, 230)
        self.img_plat_4 = QLabel(self)
        self.img_plat_4.setPixmap(QtGui.QPixmap(str(folder) + "/plat.png"))
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

######################################################################################### 

if __name__ == '__main__':
    print(folder)
    print(tessdata_path)
    print(pytesseract.pytesseract.tesseract_cmd)
    get_serv_data()
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    app = QtWidgets.QApplication(argv)
    app.setQuitOnLastWindowClosed(False)
    princ = Fenetre()
    exit(app.exec_())

# Relic rewards initialized
# check for levenstein distance correct for triggering detection