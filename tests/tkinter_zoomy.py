# source: [https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan]
# -*- coding: utf-8 -*-
# Advanced zoom example. Like in Google Maps.
# It zooms only a tile, but not the whole image. So the zoomed tile occupies
# constant memory and not crams it with a huge resized image for the large zooms.
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename


class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class Zoom_Advanced(ttk.Frame):


    ''' Advanced zoom of the image '''
    def __init__(self, mainframe): #, path):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        self.path = ''
        self.page_title_coords = []
        self.page_number_coords = []
        self.image_file = ''
        self.x1, self.y1, self.x2, self.y2 = '', '', '', ''
        self.title_rect = ''
        self.number_rect = ''

        # Vertical and horizontal scrollbars for canvas
        vbar = tk.Scrollbar(self.master, orient='vertical')
        hbar = tk.Scrollbar(self.master, orient='horizontal')
        vbar.grid(row=3, column=5, sticky='ns')
        hbar.grid(row=4, column=0, columnspan=4, sticky='we')

        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set,
                                width=1200, height=800, scrollregion=(0,0,1200,800))
        self.canvas.grid(row=3, column=0, columnspan=4, sticky='nsew')
        #self.canvas.addtag("all")
        self.canvas.update()  # wait till canvas is created

        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        

        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.set_standard_bindings()

                # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, 1200, 800, width=0)
        #self.width, self.height = 0, 0
        self.imscale = 1.0  # scale for the canvas image
        self.delta = 1.3  # zoom magnitude
        self.load_pic()

    def on_mousewheel_y(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.show_image()
    def on_mousewheel_x(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        self.show_image()

    def set_standard_bindings(self):
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<Control-MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_y)
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_mousewheel_x)

    def load_pic(self):
        self.path = askopenfilename(initialdir="C:/",title='Choose an image.')

        self.image = Image.open(self.path)  # open image
        self.width, self.height = self.image.size

        self.show_image()


    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image


    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image


    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)


    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image


    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()


    def show_image(self, event=None):
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    # buttom functions
    def draw_title_rect(self):
        self.canvas.delete(self.title_rect)
        self.page_title_coords = []
        self.canvas.bind("<Button-1>", self.xaxis_title)
        self.canvas.bind("<ButtonRelease-1>", self.yaxis_title)
        self.canvas.bind("<B1-Motion>",self. motionBox_title)
    def draw_number_rect(self):
        self.canvas.delete(self.number_rect)
        self.page_number_coords = []
        self.canvas.bind("<Button-1>", self.xaxis_number)
        self.canvas.bind("<ButtonRelease-1>", self.yaxis_number)
        self.canvas.bind("<B1-Motion>", self.motionBox_number)
    def store_title_coords(self):
        print(self.page_title_coords)
    def store_number_coords(self):
        print(self.page_number_coords)
    def reset_title(self):
        # delete title rectangle & reset coords
        self.page_title_coords = []
        self.canvas.delete(self.title_rect)
    def reset_number(self):
        self.page_number_coords = []
        self.canvas.delete(self.number_rect)

    def printcoords(self, event):
        print (event.x,event.y)
    def xaxis_title(self, event):
        self.x1, self.y1 = (event.x - 1), (event.y - 1)
        self.title_rect = self.canvas.create_rectangle(self.x1, self.y1, self.x1,
                                            self.y1, activeoutline='black')
    def xaxis_number(self, event):
        self.x1, self.y1 = (event.x - 1), (event.y - 1)
        self.number_rect = self.canvas.create_rectangle(self.x1, self.y1,
                                            self.x1, self.y1, activeoutline='black')
    def motionBox_title(self, event):
        self.x2, self.y2 = (event.x + 1), (event.y + 1)
        self.canvas.coords(self.title_rect, self.x1, self.y1, self.x2, self.y2)
    def motionBox_number(self, event):
        self.x2, self.y2 = (event.x + 1), (event.y + 1)
        self.canvas.coords(self.number_rect, self.x1, self.y1, self.x2, self.y2)
    def yaxis_title(self, event):
        self.x2, self.y2 = (event.x + 1), (event.y + 1)
        print("Stored coords: {}, {}, {}, {}".format(self.x1, self.y1, self.x2, self.y2))
        self.canvas.coords(self.title_rect, self.x1, self.y1, self.x2, self.y2)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.set_standard_bindings()
        self.x1, self.y1, self.x2, self.y2 = self.canvas.coords(self.title_rect)
        #convert window coords to canvas coords
        # see https://effbot.org/tkinterbook/canvas.htm#coordinate-systems
        # use canvasx & canvasy
        self.page_title_coords = [self.x1, self.y1, self.x2, self.y2]
    def yaxis_number(self, event):
        self.x2, self.y2 = (event.x + 1), (event.y + 1)
        print("Stored coords: {}, {}, {}, {}".format(self.x1, self.y1, self.x2, self.y2))
        self.canvas.coords(self.number_rect, self.x1, self.y1, self.x2, self.y2)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.set_standard_bindings()
        self.x1, self.y1, self.x2, self.y2 = self.canvas.coords(self.number_rect)
        self.page_number_coords = [self.x1, self.y1, self.x2, self.y2]
'''
path = r'C:\\Users\\Josh\\Pictures\\goldie hawn 2.jpg'  # place path to your image here
root = tk.Tk()
app = Zoom_Advanced(root, path=path)
root.mainloop()
'''