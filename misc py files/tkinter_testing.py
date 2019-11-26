from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

def load_pic():
    global abs_path
    global image_file
    abs_path = askopenfilename(master=root, initialdir="C:/",title='Choose an image.')
    pic = Image.open(abs_path)
    crop_coor = (pic.width * 0.85, pic.height * 0.75, pic.width, pic.height)
    pic = pic.crop(crop_coor)
    image_file = ImageTk.PhotoImage(pic)
    canvas.create_image(0,0,image=image_file, anchor='nw')

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

root = Tk()
frame = Frame(root)
canvas = Canvas(canvas_frame, width=500, height=800, scrollregion=(0,0,500,800)) 
canvas.grid(row=3, column=0, columnspan=4, sticky=N+S+E+W)

x_scroll = Scrollbar(frame, orient=HORIZONTAL)
x_scroll.grid(row=4, column=0, columnspan=4, sticky=E+W)

y_scroll = Scrollbar(frame, orient=VERTICAL)
y_scroll.grid(row=3, column=5, sticky=N+S)

x_scroll.config(command=canvas.xview)
y_scroll.config(command=canvas.yview)
canvas.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, scrollregion=canvas.bbox(ALL))

# https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
scroll_window = Frame(canvas) # HERE

frame.grid(row=0)

button = Button(frame, text="QUIT", fg="red", command=frame.quit # fg is short for foreground
).grid(row=0, column=0, sticky=N+S+E+W)
button = Button(frame, text="Load", command=load_pic # fg is short for foreground
).grid(row=0, column=3, sticky=N+S+E+W)

btn_title_box = Button(frame, text="Select Page Title", command=store_title_coords
).grid(row=0, column=1, sticky=N+S+E+W)
btn_title_box_reset = Button(frame, text="Reset title box", command=reset_title
).grid(row=1, column=1, sticky=N+S+E+W)
btn_draw_title_box = Button(frame, text="Draw title box", command=draw_title_rect
).grid(row=2, column=1, sticky=N+S+E+W)

btn_number_box = Button(frame, text="Select Page Number", command=store_number_coords
).grid(row=0, column=2, sticky=N+S+E+W)
btn_number_box_reset = Button(frame, text="Reset number box", command=reset_number
).grid(row=1, column=2, sticky=N+S+E+W)
btn_draw_number_box = Button(frame, text="Draw number box", command=draw_number_rect
).grid(row=2, column=2, sticky=N+S+E+W)

page_title_coords = []
page_number_coords = []
abs_path = ''
image_file = ''
x1, y1, x2, y2 = '', '', '', ''
title_rect = ''
number_rect = ''

#canvas.create_image(0,0,image=image_file,anchor="nw")

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



#mouseclick event
#canvas.bind("<Button 1>",printcoords)
#canvas.bind("<ButtonRelease-1>", printcoords) # outputs the coords of mouse on release#canvas.bind("<Button-1>", xaxis)
#canvas.bind("<Button-1>", xaxis)
#canvas.bind("<ButtonRelease-1>", yaxis)
#canvas.bind("<B1-Motion>", motionBox)
#canvas.bind("<ButtonRelease-1>", draw)
root.mainloop()

#root = Tk()

# path = r'C:\Users\Josh\Drawings\2019\Q1\24 - WCDT Block 23\Tender Docs\Drawings\Converted'
'''
image_file = ''
abs_path = ''
#image_name = 'Combined Drawings(2).tif'
#pic_abs_path = ''.join([path, '\\', image_name])

frame = Frame(root) # frame is a simple container

canvas = Canvas(frame)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
frame.pack(fill=BOTH, expand=1)# pack to make it visible


button = Button(
    frame, text="QUIT", fg="red", command=frame.quit # fg is short for foreground
).grid(row=1, column=0, sticky=W)
#self.button.pack(side=LEFT)

load_image = Button(frame, text="Load Image", command=load_pic).grid(row=1, column=1, sticky=E)
#self.load_image.pack(side=LEFT)

#self.image = ImageTk.BitmapImage(App.load_pic(pic_abs_path))
#self.panel = Label(master, image=self.image)
#self.panel.pack()




 


root.mainloop() # runs the window
'''

'''
if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root) #, bd=2, relief=SUNKEN)
    #frame.grid_rowconfigure(0, weight=1)
    #frame.grid_columnconfigure(0, weight=1)
    #xscroll = Scrollbar(frame, orient=HORIZONTAL)
    #xscroll.grid(row=1, column=0, sticky=E+W) # set to bottom row and 
    #yscroll = Scrollbar(frame)
    #yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame) #, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    #xscroll.config(command=canvas.xview)
    #yscroll.config(command=canvas.yview)
    frame.pack() #fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(initialdir="C:/",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    # canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        print (event.x,event.y)
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()
    
    '''