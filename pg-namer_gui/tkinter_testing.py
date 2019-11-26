import os, sys
sys.path.append(os.path.realpath('page_namer/custom libs')) # add local dir to import path
sys.path.append(os.path.realpath('page_namer/tests')) 
from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
from tkinter_zoomy import Zoom_Advanced

'''
def load_pic():
    global abs_path
    global image_file
    abs_path = askopenfilename(master=root, initialdir="C:/",title='Choose an image.')
    pic = Image.open(abs_path)
    crop_coor = (pic.width * 0.85, pic.height * 0.75, pic.width, pic.height)
    #pic = pic.crop(crop_coor)
    image_file = ImageTk.PhotoImage(pic)
    canvas.create_image(0,0,image=image_file, anchor='nw')
    canvas.config(scrollregion=(0,0,pic.width, pic.height))

def draw_title_rect():
    global canvas, title_rect, page_title_coords
    canvas.delete(title_rect)
    page_title_coords = []
    canvas.bind("<Button-1>", xaxis_title)
    canvas.bind("<ButtonRelease-1>", yaxis_title)
    canvas.bind("<B1-Motion>", motionBox_title)
def draw_number_rect():
    global canvas, number_rect, page_number_coords
    canvas.delete(number_rect)
    page_number_coords = []
    canvas.bind("<Button-1>", xaxis_number)
    canvas.bind("<ButtonRelease-1>", yaxis_number)
    canvas.bind("<B1-Motion>", motionBox_number)
def store_title_coords():
    global page_title_coords
    print(page_title_coords)
def store_number_coords():
    global page_number_coords
    print(page_number_coords)
def reset_title():
    # delete title rectangle & reset coords
    global page_title_coords
    page_title_coords = []
    canvas.delete(title_rect)
def reset_number():
    global page_number_coords
    page_number_coords = []
    canvas.delete(number_rect)
'''

'''
#bind mousewheel [https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar]
def on_mousewheel_y(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
def on_mousewheel_x(event):
    canvas.xview_scroll(int(-1*(event.delta/120)), "units")
'''

root = Tk()
#frame = Frame(root) # replaced with Advanced_Zoom frame
frame = Frame(root)

Grid.columnconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 0, weight=1)
canvas = Zoom_Advanced(frame) #, width=1200, height=800, scrollregion=(0,0,1200,800))
# canvas.grid(row=3, column=0, columnspan=4, sticky=N+S+E+W) # grid setting moved to zoomy class
# canvas.canvas.addtag_all("all")

'''
x_scroll = Scrollbar(frame, orient=HORIZONTAL)
x_scroll.grid(row=4, column=0, columnspan=4, sticky=E+W)

y_scroll = Scrollbar(frame, orient=VERTICAL)
y_scroll.grid(row=3, column=5, sticky=N+S)

x_scroll.config(command=canvas.xview)
y_scroll.config(command=canvas.yview)
'''

'''
#bind mousewheel to scrollbars
canvas.bind_all("<MouseWheel>", on_mousewheel_y)
canvas.bind_all("<Shift-MouseWheel>", on_mousewheel_x)
'''

# canvas.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, scrollregion=canvas.bbox(ALL))

# this sets the rows and columns that are too automatically reaize when you resize the program window
# you want ALL columns to resize when you stretch the window in the X direction
for x in range(4):
    Grid.columnconfigure(frame, x, weight=1)
# but you only want the picture to resize when stretched in the Y direction, buttons to remain unchanged
Grid.rowconfigure(frame, 3, weight=1)


frame.grid(row=0, sticky=N+S+E+W)

button = Button(frame, text="QUIT", fg="red", command=frame.quit # fg is short for foreground
).grid(row=0, column=3, sticky=N+S+E+W)
button = Button(frame, text="Load", command=canvas.load_pic # fg is short for foreground
).grid(row=0, column=0, sticky=N+S+E+W)

btn_title_box = Button(frame, text="Select Page Title", command=canvas.store_title_coords
).grid(row=0, column=1, sticky=N+S+E+W)
btn_title_box_reset = Button(frame, text="Reset title box", command=canvas.reset_title
).grid(row=1, column=1, sticky=N+S+E+W)
btn_draw_title_box = Button(frame, text="Draw title box", command=canvas.draw_title_rect
).grid(row=2, column=1, sticky=N+S+E+W)

btn_number_box = Button(frame, text="Select Page Number", command=canvas.store_number_coords
).grid(row=0, column=2, sticky=N+S+E+W)
btn_number_box_reset = Button(frame, text="Reset number box", command=canvas.reset_number
).grid(row=1, column=2, sticky=N+S+E+W)
btn_draw_number_box = Button(frame, text="Draw number box", command=canvas.draw_number_rect
).grid(row=2, column=2, sticky=N+S+E+W)

page_title_coords = []
page_number_coords = []
abs_path = ''
image_file = ''
x1, y1, x2, y2 = '', '', '', ''
title_rect = ''
number_rect = ''

#canvas.create_image(0,0,image=image_file,anchor="nw")

'''
def printcoords(event):
    print (event.x,event.y)
def xaxis_title(event):
    global x1, y1, title_rect
    x1, y1 = (event.x - 1), (event.y - 1)
    title_rect = canvas.create_rectangle(x1, y1, x1, y1, activeoutline='black')
def xaxis_number(event):
    global x1, y1, number_rect
    x1, y1 = (event.x - 1), (event.y - 1)
    number_rect = canvas.create_rectangle(x1, y1, x1, y1, activeoutline='black')
def motionBox_title(event):
    global x1, y1, x2, y2, title_rect
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.coords(title_rect, x1, y1, x2, y2)
def motionBox_number(event):
    global x1, y1, x2, y2, number_rect
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.coords(number_rect, x1, y1, x2, y2)
def yaxis_title(event):
    global x1, y1, x2, y2, title_rect, canvas, page_title_coords
    x2, y2 = (event.x + 1), (event.y + 1)
    print("Stored coords: {}, {}, {}, {}".format(x1, y1, x2, y2))
    canvas.coords(title_rect, x1, y1, x2, y2)
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.unbind("<B1-Motion>")
    x1, y1, x2, y2 = canvas.coords(title_rect)
    #convert window coords to canvas coords
    # see https://effbot.org/tkinterbook/canvas.htm#coordinate-systems
    # use canvasx & canvasy
    page_title_coords = [x1, y1, x2, y2]
def yaxis_number(event):
    global x1, y1, x2, y2, number_rect, page_number_coords
    x2, y2 = (event.x + 1), (event.y + 1)
    print("Stored coords: {}, {}, {}, {}".format(x1, y1, x2, y2))
    canvas.coords(number_rect, x1, y1, x2, y2)
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.unbind("<B1-Motion>")
    x1, y1, x2, y2 = canvas.coords(number_rect)
    page_number_coords = [x1, y1, x2, y2]
'''


#mouseclick event
#canvas.bind("<Button 1>",printcoords)
#canvas.bind("<ButtonRelease-1>", printcoords) # outputs the coords of mouse on release#canvas.bind("<Button-1>", xaxis)
#canvas.bind("<Button-1>", xaxis)
#canvas.bind("<ButtonRelease-1>", yaxis)
#canvas.bind("<B1-Motion>", motionBox)
#canvas.bind("<ButtonRelease-1>", draw)
root.mainloop()

#root = Tk()

