#for naming the files
from datetime import datetime
import fnmatch
import os

#data processing packages
import numpy as np

#monitoring the screen
from PIL import ImageGrab

#for handling mouse events
from pynput import mouse

#setting up the coordinates for the logos and shit
dislike_logo = [1058, 844, 1151, 936]
like_logo = [1241, 846, 1336, 940]
tinder_color_coord = (228, 147)
tinder_logo_color = np.array([254, 67, 88])

#creating a filename with today's date
filename = datetime.today().strftime("%Y-%m-%d") + ".txt"

def check_files(filename):
    """Checks if the file with today's date already exists. If it does it reads it's data and returns it."""

    for f_name in os.scandir():
        
        if fnmatch.fnmatch(f_name, filename):
            with open(f_name, 'r') as file:
                
                next(file)
                data = list(map(
                    int,
                    file.readline().split('\t')
                ))

            return data
        else:
            return [0, 0]

def update_swipes(swipes, x, y):
    """Updates the number of left and right swipes after each click"""

    global like_logo, dislike_logo

    if (x > like_logo[0] and x < like_logo[2]) and (y > like_logo[1] and y < like_logo[3]):
        swipes[1] +=1
    
    if (x > dislike_logo[0] and x < dislike_logo[2]) and (y > dislike_logo[1] and y < dislike_logo[3]):
        swipes[0] += 1

    return swipes

def check_tinder():
    """Checks if we are looking at tinder"""

    global tinder_color_coord, tinder_logo_color

    im = ImageGrab.grab()

    comp_arr = np.asarray(im.getpixel(xy=tinder_color_coord)) == tinder_logo_color

    if np.all(comp_arr):
        return True
    else:
        return False

def on_click(x, y, button, pressed):

    global tinder_color_coord, tinder_logo_color, swipes

    if pressed:
        if check_tinder():
            swipes = update_swipes(swipes, x, y)
        
        #if we close tinder the listening stops
        if x > 1866 and x < 1915 and y > 1 and y < 51:
            return False

swipes = check_files(filename)

#turning on mouse sensing
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

data_to_write = [
    "left swipes    right swipes\n",
    "{0}    {1}\n".format(swipes[0], swipes[1])
]

with open(filename, 'w') as file:
    file.writelines(data_to_write)

#TODO
# writing the total to a total_swipes.txt correctly