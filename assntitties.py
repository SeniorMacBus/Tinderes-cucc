#data processing packages
import numpy as np

#monitoring the screen
from PIL import ImageGrab

#for handling mouse events
from pynput import mouse

#setting up the coordinates for the logos and shit
# tinder_logo = [4, 110, 465, 194]
dislike_logo = [1058, 844, 1151, 936]
like_logo = [1241, 846, 1336, 940]

tinder_color_coord = (245, 146)
# like_color_coord = (1283, 864)
# dislike_color_coord = (1099, 861)

tinder_logo_color = np.array([254, 69, 85])
# like_color = np.array([34, 207, 125])
# dislike_color = np.array([254, 69, 85])

#list for storing the number of left and right swipes
swipes = [0, 0]
labels = ["dislikes", "likes"]

def update_swipes(swipes, x, y):
    """Updates the number of left and right swipes after each click"""

    global like_logo, dislike_logo

    l = 0
    r = 0

    if x > like_logo[0] and x < like_logo[2] and y > like_logo[1] and y < like_logo[3]:
        r += 1
    
    if x > dislike_logo[0] and x < dislike_logo[2] and y > dislike_logo[1] and y < dislike_logo[3]:
        l += 1
    
    swipes[0] = l
    swipes[1] = r

    return swipes

def check_tinder():
    """Checks if we are looking at tinder"""

    global tinder_color_coord, tinder_logo_color

    im = ImageGrab.grab()

    if np.asarray(im.getpixel(xy=tinder_color_coord)) == tinder_logo_color:
        return True
    else:
        return False

def on_click(x, y, button, pressed):

    global tinder_color_coord, tinder_logo_color, swipes

    if pressed:

        if check_tinder():
            swipes = update_swipes(swipes, x, y)
        
        if x > 1866 and x < 1915 and y > 1 and y < 51:
            return False

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
    
print(swipes)





















#TODO
#ha nincs ott nem a tindert nézzük és nem fut a program, ha igen akkor processel
#megnézni hol van a like és a dislike button a képernyőn
#amikor kattint ezt a kettőt megnézni és eldönteni melyikre kattintott
#hozzáadni a likehoz/dislikehoz egy értéket
#a kattintás után várni 0.5 másodpercet és csekkolni, hogy Match-e
#ábrázolni plotly-ban date szerint hogy mennyi lef és mennyi right swipe volt