

from PIL import Image
import pytesseract

# add tesseract path for call, otherwise it returns 'tesseract not installed or in path' error
# not sure why because I've added it to the path also ...
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
#image = Image.open(r'C:\Users\Josh\Documents\my_programs\python\ocr_test2.png')

#image_text = pytesseract.image_to_string(image)
#print(image_text)
test_dict = {1: 'fun', 2: 'doom', 3: 'crime'}
omg = [1, 4]
test = ['buns', 'bees', '', 'bombs']
for x in range(len(test_dict)):
    if x+1 not in omg:
        print(str(x+1) + ': ' + test_dict[x+1])
    '''
    if not x:
        print('EMPTY')
        continue
    else:
        print(x)
    print('end of loop')
    '''