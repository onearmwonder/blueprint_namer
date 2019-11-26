# for validate data entry for page namer
# input to validate: drawing path, pg number coor, pg title coordinate (same as number), screen choice (only 1 to 3 for options)
import os

def valid_int_list(input_list):
    # fed a list and on "exception" variable so messages can be printed if it returns false
    for x in range(len(input_list)):
        try:
            #print("Testing: ", int_list[x])
            int(input_list[x])
            #print(test)
        except Exception:
            print("\nERROR: That's not an integer! Try again. You can't use ", "'", input_list[x], "'")
            input("Press enter to continue.")
            break
        print("Coordinate", x, "confirmed!")
        if x == 3:
            print("Looks good! ")
            return True # proper list contents confirmed


def valid_list(input_string):
    try:
            list_x = input_string.split()
            if isinstance(list_x, list):
                return list_x
    except Exception:
        print("\nERROR: Please use list format and try again. Proper format: x1 y1 x2 y2")
        input("Press enter to continue.")
        return False


def valid_length(input_list, length):
    if len(input_list) == int(length):
        return True
    elif len(input_list) < int(length):
        print("\nERROR: You need four points to form a rectangle, try again. Proper format: x1 y1 x2 y2")
        input("Press enter to continue.")

        


def valid_path():
    while True:
        try:
            path = input()
            os.listdir(path)
        except FileNotFoundError:
            print("\nERROR: File not found. Please try again.")
            input("Press enter to continue.")
            continue
        if path == '':
            print("\nERROR: Please enter an actual value and try again.")
            input("Press enter to continue.")
            continue
        else:
            print("Looks good I guess, let's confirm.")
            return path


def valid_range_inclusive(min, max, message):
    while True:
        print(message)
        try:
            value = input()
            value = int(value)
        except ValueError:
            print("\nERROR: Value needs to be an integer.")
            input("Press enter to continue.")
            continue
        if value < min or value > max:
            print("\nERROR: Out of range, please enter a number between", min, "and", max, "and try again.")
            input("Press enter to continue.")
            continue
        else:
            print("Looks good.")
            return value
