# takes the converted .tif files and reads the name from them using OCR?

from __future__ import absolute_import, print_function
import os, sys, time

from PIL import Image
import pytesseract
import ctypes
from pynput import mouse, keyboard
import collections

# add path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# keyboard and mouse controllers
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

#path = os.path.abspath(r'C:\Users\Josh\Drawings\2019\Q1\24 - WCDT Block 23\Tender Docs\Drawings\Converted')
path = os.path.abspath(r'C:\Users\Josh\Drawings\2019\Q1\23 - TDI Claims Reno\Tender Docs\Drawings\Converted')
print(path)

drawings = [] # change: list of dicts, dict format = {'id': id, 'set_name': set_name, 'dwg_path': dwg_path, 'page_number': page_number, 'page_title': page_title} # (number, file_name)
drawing_set = {} # for when multiple drawing sets are loaded, key value = {'set_name': int(length)}
dwg_titles = {} # (number, page name), page name which has been parsed by the program

# use the drawings list object and add dictionary objects for each separate page
# dict format = {'id': id, 'set_name': set_name, 'dwg_path': dwg_path, 'page_number': page_number, 'page_title': page_title}
def get_tif_file_numbers():
    prev_page_set = ''
    for file in os.listdir(path):
        if file.endswith('.tif'):
            number, set_name = '', ''
            dwg_path = ''.join([path, '//', file])
            collect = False

            for x in range(len(file)):
                if file[x] == '(':
                    collect = True
                    if prev_page_set == '':
                        set_name = file[:x]
                        #print('first set!')
                        drawing_set[set_name] = 1
                    elif file[:x] == prev_page_set:
                        set_name = file[:x] # separates drawing name from file name for checking/comparing of drawing sets
                        drawing_set[set_name] = drawing_set[set_name] + 1 # increments the page counter in dwg set dict
                        #print(drawing_set[set_name])
                    else:
                        set_name = file[:x]
                        #print('new set!, prev set: {}'.format(prev_page_set))
                        drawing_set[set_name] = 1
                elif file[x] == ')':
                    collect = False
                if collect == True:
                    try:
                        y = int(file[x]) # try to convert to integer, first item is always '('
                                # so this will throw error on that only, separating it out
                        number = number + str(y)
                    except ValueError:
                        pass
            # dict format = {'id': id, 'set_name': set_name, 'path': path, 'page_number': page_number, 'page_title': page_title}
            # page_title and page_number will be added separately in OCR function
            drawings.append({'id': int(number), 'set_name': set_name, 'dwg_path': dwg_path})
            prev_page_set = set_name # to be compared with on next iteration of loop
    print("Drawings set parsed: {}".format(drawing_set))
    print("{} drawing files parsed.".format(len(drawings)))
    


def order_page_set_ids():
    number = 1
    sets = []
    set_order_index = [] # index values corresponding to sets list
    if len(drawing_set) == 1:
        pass # pass if only one drawing set
    else:
        print("\n-------------------------------------------------------------------------------------------------\n")
        print("Please indicated the order of the drawings set in OST, page names will be input in this order.")
        print("Please order by the labelled number. Order input example: 1,2,3 OR 213")
        for x in drawing_set.keys():
            sets.append(x)
            print("{} : {}".format(number, x))
            number += 1
        set_order = input("Order: ")
        for x in set_order:
            try:
                x = int(x)
                set_order_index.append(x-1)
            except ValueError:
                pass
        #print("set order index: {}".format(set_order_index))
        #print("sets list: {}".format(sets))

        # for each drawing set listed in sets, change ID base on given order
        # for each drawing read its set name and check that names position in the set_order_index
        # when match is found sum the drawing_set page total for each previous index value
        for x in drawings:
            for y in range(len(sets)):
                id_offset = 0
                if x['set_name'] == sets[set_order_index[y]]:
                    if y == 0: # if first set in order dont change ID
                        continue
                    else:
                        for z in range(y):
                            id_offset += drawing_set[sets[set_order_index[z]]]
                    x['id'] = x['id'] + id_offset


def get_dwg_names():
    failed_pages = [] # holds id's of failed pages
    # loop through images in dwg_numbers_dict
    # crop the image twice, once onto the number block and once onto the title block
    # use tesseract OCR to read the number and title
    # combine number and title and store into dwg_titles_dict
    for x in drawings:
        if x['id'] == '1':
            x['page_title'] = 'Cover'
            x['page_number'] = ''
            x['combined_title'] = x['page_title']
            continue
        else:
            number_crop = Image.open(x['dwg_path']).crop(page_number_coor)
            title_crop = Image.open(x['dwg_path']).crop(page_title_coor)

            # use OCR to read the crops
            number_crop_text = pytesseract.image_to_string(number_crop)
            title_crop_text = pytesseract.image_to_string(title_crop)
            print("Reading page: {}".format(x['id']))
            # remove empty strings and log the files that had them missed
            if not number_crop_text or not title_crop_text:
                failed_pages.append(x['id'])
                x['page_title'] = 'FAILED AUTO READ'
                x['page_number'] = ''
                x['combined_title'] = x['page_title']
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

            x['page_title'] = title_crop_text
            x['page_number'] = number_crop_text
            x['combined title'] = combined_title
         
            print(x['id'])


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
    mouse_controller.position = (screensize[0] / 2, 15)
    mouse_controller.press(mouse.Button.left)
    mouse_controller.release(mouse.Button.left)
    time.sleep(0.1)
    keyboard_controller.press(keyboard.Key.home)
    time.sleep(0.1)
    alt_press('e')
    time.sleep(0.1)
    alt_press('n')

def enter_page_names():
    open_page_rename_field()
    for x in range(len(drawings)):
        page = list((page for page in drawings if page['id'] == x+1))
        print("Entering page: ", page)
        keyboard_controller.type(page[0]['combined_title'])
        time.sleep(0.2) # minor delay so OST can keep up
        ctrl_enter_press()


def name_pages():
    get_tif_file_numbers()
    order_page_set_ids() # resets page IDs in correct order
    get_dwg_names()
    enter_page_names()

# retrieve page numbers & titles from tif files for cropping
page_number_coor = [9262, 6776, 9738, 7017]
page_title_coor = [9264, 6267, 9960, 6507]


name_pages()
'''
for x in range(len(drawings)):
    # need to list because this makes a generator object which cant be printed outright
    page = list((page for page in drawings if page['id'] == x+1))
    print(page[0])

'''



