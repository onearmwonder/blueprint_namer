# todo
# allow to be run from cmd, accept inputs for page coordinates, drawing path
# check for required packages on startup and install as needed
# drawing parser only reads the ".tif" and the number between the brackets: (1).tif, so multiple set don't work
#       right now, multiple 1s and 2s and so on are read and only one name is applied to all
# ----------------------------------------


# before using, install: pillow (for PIL), pytesseract (pip install pytesseract) & the tesseract-ocr base from:
#  https://github.com/UB-Mannheim/tesseract/wiki, pynput from pip

# takes the converted .tif files and reads the name from them using OCR?

from __future__ import absolute_import, print_function
import os, sys, time

from PIL import Image
import pytesseract
import ctypes
from pynput import mouse, keyboard
import collections

# retrieve page numbers & titles from tif files
page_number_coor = [9525, 7540, 10240, 7720]
page_title_coor = [9520, 7120, 10275, 7360]

# add path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Josh\AppData\Local\Tesseract-OCR\tesseract.exe'

page_order_list = [] # ordered list of keys to reference name dictionary in the right order
drawings = {} # (number, file_name)
dwg_titles = {} # (number, page name), page name which has been parsed by the program

path = os.path.abspath(r'S:\Blueprints\Garneau Residential Development\Tender Docs\Drawings\Converted')

# keyboard and mouse controllers
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

print(path)

# use the drawings dictionary object and add the drawing number and file path
# as a key value pair (number, file_name)
def get_tif_file_numbers(path, drawings_dict, order_list):
    for im in os.listdir(path):
        if im.endswith('.tif'):
            number = ''
            collect = False
            for x in im:
                if x == '(':
                    collect = True
                elif x == ')':
                    collect = False
                if collect == True:
                    try:
                        y = int(x) # try to convert to integer, first item is always '('
                                # so this will throw error on that only, separating it out
                                # not pretty, learn regex you savage
                        number = number + str(y)
                    except ValueError:
                        pass
            drawings[number] = ''.join([path, '//', im])
            order_list.append(number)
    order_list = [int(x) for x in order_list]
    order_list = sorted(order_list)
    print("{} drawing files parsed.".format(len(drawings_dict)))
    return order_list, drawings_dict


def get_dwg_names(path, dwg_numbers_dict, dwg_num_coor, dwg_title_coor):
    # take file numbers dictionary and drawing coordinates of the dwg's title
    # and number blocks and read them and store them into the dwg_titles dictionary for
    # OST input
    dwg_title_dict = {}
    failed_pages = {}
    # TODO: loop through images in dwg_numbers_dict
    #           crop the image twice, once onto the number block and once onto the title block
    #           use tesseract OCR to read the number and title
    #           combine number and title and store into dwg_titles_dict
    for x in dwg_numbers_dict:
        if x == '1':
            dwg_title_dict[x] = 'Cover'
            continue
        else:
            number_crop = Image.open(drawings[x]).crop(page_number_coor)
            title_crop = Image.open(drawings[x]).crop(page_title_coor)

            # use OCR to read the crops
            number_crop_text = pytesseract.image_to_string(number_crop)
            title_crop_text = pytesseract.image_to_string(title_crop)

            # remove empty strings and log the files that had them missed
            if not number_crop_text or not title_crop_text:
                failed_pages[x] = dwg_numbers_dict[x]
                dwg_title_dict[x] = 'FAILED AUTO READ'
                continue # stops loop here, move onto next item

            # string cleaning
            title_crop_text = title_crop_text.title()            
            title_crop_text = title_crop_text.strip()
            
            number_crop_text = number_crop_text.replace('Z', '7') # &'s get mistaken for Z's by OCR commonly
            number_crop_text = number_crop_text.replace('$', 'S')
            number_crop_text = number_crop_text.replace('O', '0')
            number_crop_text = number_crop_text.replace('l', '1')
            number_crop_text = number_crop_text.replace('|', '')
            number_crop_text = number_crop_text.strip()
            
            # ADDS IN DECIMAL TO PAGE NUMBER IF MISSED BY OCR, ADJUST BASED ON PAGE NUMBER FORMAT, MAYBE HAVE DIFFERENT PREMADE FORMATS FOR DIFFERENT ARCH'S???
            if len(number_crop_text) > 3:
                if number_crop_text[2] != '.' and number_crop_text[3] != '.':
                    if len(number_crop_text) == 4:
                        number_crop_text = number_crop_text[:2] + '.' + number_crop_text[2:]
                    elif len(number_crop_text) == 5:
                        number_crop_text = number_crop_text[:3] + '.' + number_crop_text[3:]


            combined_title = number_crop_text + ' - ' + title_crop_text
            
            # overall title cleanup
            combined_title = combined_title.replace('\n', ' ')


            dwg_title_dict[x] = combined_title
         
            print(x)




    return dwg_title_dict


# controlling mouse and keyboard w/ pynput for page name insertion into OST
def get_screen_size():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    return screensize

def alt_press(key):
    with keyboard_controller.pressed(keyboard.Key.alt):
        keyboard_controller.press(key)
def ctrl_enter_press():
    with keyboard_controller.pressed(keyboard.Key.ctrl):
        keyboard_controller.press(keyboard.Key.enter)

def open_page_rename_field():

    # selects exposed header bar of center screen program
    input('''Please make sure that the OST window is full-screen on center monitor. Then press ENTER.\n
    WARNING: you cannot click or touch your mouse during operation. 
    Please wait for program to finish before selecting anything else''')
    screensize = get_screen_size()
    mouse_controller.position = (screensize[1] / 2, 15) 
        #    screensize[x] is the selected screen, check display settings for which screen you need to set, [0] = 1 in settings, etc.
    mouse_controller.press(mouse.Button.left)
    mouse_controller.release(mouse.Button.left)
    keyboard_controller.press(keyboard.Key.home)
    alt_press('e')
    alt_press('n')

def enter_page_names():
    for x in page_order_list:
        print("Entering page: ", dwg_titles[str(x)])
        keyboard_controller.type(dwg_titles[str(x)])
        time.sleep(0.2)
        ctrl_enter_press()



# sort the drawing files by number

page_order_list, drawings = get_tif_file_numbers(path, drawings, page_order_list)


dwg_titles = get_dwg_names(path, drawings, page_number_coor, page_title_coor)

'''
print("Auto-read drawing list names:")
print(page_order_list)
for x in page_order_list:
    print(x, ': ', dwg_titles[str(x)])
'''



# to crop = image.crop(box), where box coordinates = (left, upper, right, lower)

# im = Image.open(''.join([path, '\\', drawings['5']]))
# im.show() # CURRENT ISSUE, OPENS FILES AS BMP IMAGE AND SOMETIMES IT JUST SAYS 
          # 'file not found, has been moved or renamed' - I DONT KNOW WHY THE FUCK THAT IS
          # if this happens open the file manually through file explorer and then it'll
          # display if you run it again


open_page_rename_field()

enter_page_names()
