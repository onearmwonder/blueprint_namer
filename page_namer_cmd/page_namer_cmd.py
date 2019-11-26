import validation
import page_namer_backend

# ----------------------------- input section
confirmed_path = ''
confirmed_pg_no_coor = []
confirmed_pg_title_coor = []
confirmed_screen = 0

#-----------------------------------

# startup info: file path, page number & title coordinates
def input_path():
    print("Please paste the absolute path to your converted drawing folder:")
    path = validation.valid_path()
    if path:
        return path
    else:
        print("ERROR: I don't know what you did but you broke something.")
        input("Press enter to continue.")
        return False
    
# uses local validation library to test the length, that all are integers, and that its a valid list
def input_coor(input_call):
    #   todo:   check that all coordinates fall inside the pic extents (later, not important)
    while True:
        print("Please enter the coordinates of the page number from the tif file (enter as a list, ex. x1 y1 x2 y2):")
        input_string = input(input_call)
        # if valid the input coordinates are saved to temp coor var. for further tests
        coor = validation.valid_list(input_string)
        if coor:
            if validation.valid_length(coor, '4'): 
                if validation.valid_int_list(coor):
                    return coor


# select a screen from 1 to 3, the system will take it as x - 1 because it starts at 0
def input_selected_screen():
    actual_screen = 0
    while True:
        message = '''Please select the screen OST is displayed on, this will be a number from 1 to 3, 
            to discover your screen numbers press the windows key OR open the start menu, 
            THEN type DISPLAY and select DISPLAY SETTINGS when it appears in the list. 
            The display settings will show the order of your screens, simply type the number of the screen 
            you are using for your OST application (Note: make sure OST is MAXIMIZED in the screen).
            \nPlease select your OST screen (Options: 1/2/3)'''
        screen = validation.valid_range_inclusive(1,3, message)
        if screen:
            actual_screen = screen - 1
            break
    return actual_screen
         

def startup(): 
    confirmed_path = input_path()
    confirmed_pg_no_coor = input_coor("Please provide the pg NUMBER coordinates.")
    confirmed_pg_title_coor = input_coor("Please provide the pg TITLE coordinates.")
    confirmed_screen = input_selected_screen()
    while True:
        startup_input = ''
        print("\n#-------------------------------#")
        print("1 : ", confirmed_path)
        print("2 : ", confirmed_pg_no_coor)
        print("3 : ", confirmed_pg_title_coor)
        print("4 : ", confirmed_screen + 1)
        print("#-------------------------------#\n")
        print('''Above is your current configuration, look it over, if anything needs to change
        simply type that lines number and press enter. Otherwise type '0' to continue.''')
        try:
            startup_input = input()
            startup_input = int(startup_input)
        except ValueError:
            print("Try again, you need to enter an integer.")
        if startup_input == 1:
            confirmed_path = input_path()
        elif startup_input == 2:
            confirmed_pg_no_coor = input_coor("Please provide the pg NUMBER coordinates.")
        elif startup_input == 3:
            confirmed_pg_title_coor = input_coor("Please provide the pg TITLE coordinates.")
        elif startup_input == 4:
            confirmed_screen = input_selected_screen()
        elif startup_input == 0:
            break
        else: 
            print("\nERROR: Number not applicable, are you alright?")
            input("Press enter to continue.")
            continue

        print("\n#-------------------------------#")
        print('''\nIMPORTANT!!! The program will begin shortly, please make sure again that
OST is maximized to the screen you selected. All data you input is now set, you cannot change 
anything once past this point.''')
        print("#-------------------------------#\n")


startup()