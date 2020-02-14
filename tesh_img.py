import cv2
import matplotlib.pyplot as plt
import numpy as np

img_file = 'my_screenshot.png'
image = cv2.imread(img_file)

# RGB Format
ui_color_list = [
    (189, 168, 101, 'Virtuvian'),   # Vitruvian
    (150, 31, 35, 'Stalker'),       # Stalker 
    (238, 193, 105, 'Baruk'),       # Baruk
    (35, 200, 245, 'Corpus'),       # Corpus
    (57, 105, 192, 'Fortuna'),      # Fortuna
    (255, 189, 102, 'Grineer'),     # Grineer
    (36, 184, 242, 'Lotus'),        # Lotus
    (140, 38, 92, 'Nidus'),         # Nidus
    (20, 41, 29, 'Orokin'),         # Orokin
    (9, 78, 106, 'Tenno'),          # Tenno
    (2, 127, 217, 'High contrast'), # High contrast
    (255, 255, 255, 'Legacy'),      # Legacy
    (158, 159, 167, 'Equinox')      # Equinox
]

# Check ui theme from screenshot
def check_pix(input_pix_clr, input_theme, color_treshold):
    e = (189, 168, 101, 'Virtuvian')
    if abs(input_pix_clr[2] - e[0]) < color_treshold and abs(input_pix_clr[1] - e[1]) < color_treshold and abs(input_pix_clr[0] - e[2]) < color_treshold:
        return True
    else:
        return False
            
def tresh(image):
    ui_color = (189, 168, 101)
    h = image.shape[0] # Hauteur
    w = image.shape[1] # Largeur
    for y in range(0, h):
        for x in range(0, w):
            pix_crl = image[y, x]
            if check_pix(pix_crl, 'Virtuvian', max([ui_color[0], max([ui_color[1], ui_color[2]])]) / 7 + 30) is True:
                image[y, x] = (0, 0 ,0)
            else:
                image[y, x] = (255, 255 ,255)
    
    return image
            
image2 = tresh(image)
# imgtresh_temp = tresh(image2)
# kernel = np.ones((1, 1), np.uint8)
# imgtresh = cv2.erode(imgtresh_temp, kernel, iterations=1)
    
cv2.imwrite('test.png', image2)