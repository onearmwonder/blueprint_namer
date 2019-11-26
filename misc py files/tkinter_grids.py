from tkinter import *
from PIL import ImageTk, Image

root = Tk()
''' simple layout
Label(root, text="First").grid(row=0)
Label(root, text="Second").grid(row=1)


Label(root, text="First").grid(row=0, sticky=W) # sticky moves objects to a side of their specific grid cell, centered by default
Label(root, text="Second").grid(row=1, sticky=W)
'''

label1 = Label(root, text="Height:").grid(sticky=E)
label2 = Label(root, text="Width:").grid(sticky=E)

e1 = Entry(root).grid(row=0, column=1)
e2 = Entry(root).grid(row=1, column=1)

checkbutton = Checkbutton(root).grid(columnspan=2, sticky=W)

img = ImageTk.PhotoImage(Image.open(r'C:\Users\Josh\Documents\my_programs\python\ocr_test2.png'))
image = Image(root, image=img).grid(row=0, column=2, columnspan=2, rowspan=2,
                sticky=W+E+N+S, padx=5, pady=5)

root.mainloop()



