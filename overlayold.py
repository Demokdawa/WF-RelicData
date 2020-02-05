from tkinter import *
import win32api
import win32con
import pywintypes


def show_overlay(rel_values):
    master = Tk()
    master.geometry('1920x1080')
    master.wm_attributes("-alpha", 0)
    labels = []
    for e in rel_values:
        label = Label(master, text=e[0], font=('Roboto', '30'), fg='black', bg='white')
        # label.master.overrideredirect(True)
        # label.master.geometry('+' + str(e[2]) + '+' + str(e[3]))
        label.place(x=e[2], y=e[3])
        label.master.lift()
        #label.master.wm_attributes("-topmost", True)
        label.master.wm_attributes("-disabled", True)
        # label.pack()
        labels.append(label)
    print(labels)
    master.mainloop()



    #label_1 = tkinter.Label(text=str(plats) + ' ' + str(ducats), font=('Roboto', '30'), fg='black', bg='white')
    #label_1.master.overrideredirect(True)
    #label_1.master.geometry('+' + str(pos1) + '+' + str(pos2))
    #label_1.master.lift()
    #label_1.master.wm_attributes("-topmost", True)
    #label_1.master.wm_attributes("-disabled", True)
    # label.master.wm_attributes("-transparentcolor", "white")

    #hWindow = pywintypes.HANDLE(int(label_1.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    #exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    #win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    #label_1.pack()
    #label_1.mainloop()
