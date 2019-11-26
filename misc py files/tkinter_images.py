from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image    

def showImage():
        lbl1.configure(image=image_tk)
        btn.configure(text = "load image!", command=showImage1)

def showImage1(): 
        lbl1.configure(image=image_tk1)
        btn.configure(text = "load image!", command=showImage)     

root = Tk()    
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

fname = r"C:\Users\Josh\Documents\my_programs\python\ocr_test.png"
image_tk = ImageTk.PhotoImage(Image.open(fname))

fname1 = r"C:\Users\Josh\Documents\my_programs\python\ocr_test2.png"
image_tk1 = ImageTk.PhotoImage(Image.open(fname1))  # new image object


btn = ttk.Button(c, text="load image", command=showImage)
lbl1 = ttk.Label(c)
btn.grid(column=0, row=0, sticky=N, pady=5, padx=5)
lbl1.grid(column=1, row=1, sticky=N, pady=5, padx=5)

root.mainloop()