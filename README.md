# blueprint_namer

application to open and read pdf files, identifying the title block and using OCR to read the page number and name

currently used as a macro for on screen takeoff, path reads the converted .tif files output by on screen takeoff's conversion from pdf format

CURRENTLY DOES NOT READ PDFS AS OCR WILL NOT WORK ON THE BINARY, unless your smarter than me

currently i'm working on the command line version of it, though there is a tkinter half-baked in here too (unfinished), command line requires input: path to image files (converted from pdf), coordinates on image of page number, coordinates to title, and the screen your application is running for the macro to function

eventually we will have
  - optional macro and instead simply rename the image files by default (probably easy)
  - converter for one big pdf file into separate pdf pages into .tif image files
  - title block indentifier (sounds hard)
  - then all at once: you feed it a pdf file, it separates it into idividual pages and converts to desired format (.tif to start) and names the files all at once
  
  
TODO now
- write code into classes for the cmd line variant
- add automatic rename of image files
- image conversion (speed?)
