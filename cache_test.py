        
'''
number_crop_text = 'A0.03'          
print("number_crop_text[2] = ", number_crop_text[2])
print("number_crop_text[3] = ", number_crop_text[3])
print("text length = ", len(number_crop_text))

if len(number_crop_text) > 3:
    if number_crop_text[2] != '.' and number_crop_text[3] != '.':
        if len(number_crop_text) == 4:
            number_crop_text = number_crop_text[:2] + '.' + number_crop_text[2:]
        elif len(number_crop_text) == 5:
            number_crop_text = number_crop_text[:3] + '.' + number_crop_text[3:]


print(number_crop_text)
'''
import os
path = os.path.abspath(r'C:\Users\Josh\Drawings\2019\Q1\24 - WCDT Block 23\Tender Docs\Drawings\Converted')
file_path = ''.join([path, '//', r'test.txt'])
'''
for files in os.listdir(path):
    if files == 'test.txt':
        print(files)
'''
# read the file
file = open(file_path, 'r')
print(file.read())
file.close()
# write to the file
file = open(file_path, 'w')
words = ['bins', 'buns', 'bombs', 'bees', 'bessie is a goddess']
for x in words:
    file.write(''.join([x, '\n']))


file.close()
file = open(file_path, 'r')
print("read from file")
read_file = file.read()
print(read_file)

print("using readline()")
for x in range(10):
    print(file.readline())
file.close()



