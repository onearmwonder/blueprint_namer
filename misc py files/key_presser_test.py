from pynput import mouse, keyboard

import time

'''
#get screen width with tkinter, ONLY READS SIZE OF PRIMARY MONITOR 
import tkinter as tk
root = tk.Tk()
tk_screen_width = root.winfo_screenwidth()
tk_screen_height = root.winfo_screenheight()
print("tk read screen size: {}, {}".format(tk_screen_height, tk_screen_width))

# get primary screen size using pywin32
from win32api import GetSystemMetrics
print("win32api width,0 = ", GetSystemMetrics(0))
print("wind32api height, 1 = ", GetSystemMetrics(1))

# get virtual screen size (bounding box for all monitors) using pywin32
from win32api import GetSystemMetrics
print("virtual screen width using win32api = ", GetSystemMetrics(78))
print("virtual screen height using win32api = ", GetSystemMetrics(79))
'''

# or use ctypes instead of pywin32
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
print("virtual screen size using ctypes bb = ", screensize)



mouse1 = mouse.Controller()
keyboard1 = keyboard.Controller()

# read mouse position
print('The mouse pointer is currently at: {0}'.format(mouse1.position))

# move mouse position
mouse1.position = (screensize[0] / 2, 15)
print('The mouse pointer has been moved to: {0}'.format(mouse1.position))

# move to a relative position
#time.sleep(1)
#mouse1.move(50, -80)

# press & release
mouse1.press(mouse.Button.left)
mouse1.release(mouse.Button.left)

def alt_press(key):
    with keyboard1.pressed(keyboard.Key.alt):
        keyboard1.press(key)
def ctrl_enter_press():
    with keyboard1.pressed(keyboard.Key.ctrl):
        keyboard1.press(keyboard.Key.enter)

names = ['first', 'second', 'third', '4th', 'next', 'again', 'again', 'stop', 'you work me so hard', 'omg miyagi why?']
alt_press('e')
alt_press('n')
for x in names:
    keyboard1.type(x)
    ctrl_enter_press()
