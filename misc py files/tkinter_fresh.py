# another attempt at tkinter image loading
from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

def LoadImage():
    global image_path 
    global image_tk
    image_path = askopenfilename(initialdir="C:/", title='Choose an Image.')
    image_tk = ImageTk.PhotoImage(Image.open(image_path))
    image_label.configure(image=image_tk)

root = Tk()
frame = ttk.Frame(root).grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

x1, y1, x2, y2 = '', '', '', ''
image_path = ''
image_tk = ''

load_btn = ttk.Button(frame, text="Load Image", command=LoadImage)
image_label = ttk.Label(frame)

load_btn.grid(column=0, row=1)
image_label.grid(column=0, row=0)

def printcoords(event):
    print(event.x, event.y)
def xaxis(event):
    global x1
    global y1
    x1, y1 = (event.x - 1), (event.y - 1)
def yaxis(event):
    global x2
    global y2
    x2, y2 = (event.x + 1), (event.y + 1)


image_label.bind("<Button-1>", printcoords) # outputs coordinates of mouse on press
image_label.bind("<ButtonRelease-1>", printcoords) # outputs the coords of mouse on release
image_label.bind("<Button-1>", xaxis)
image_label.bind("<ButtonRelease-1>", yaxis)
root.mainloop()