from datetime import datetime
from PIL import Image, ImageTk
import tkinter as Tk
import random, sys

# TKINTER!!!!
root = Tk.Tk()

# Makes him go away temporarily while setup happens
root.geometry('1x1+10000+10000')

# Constants
SW = root.winfo_screenwidth() # Screen Width
SH = root.winfo_screenheight() # Screen Height
IW = int(SW * 0.12) # Image Width
IH = int(SH * 0.09) # Image Height
Y_MAX = int(SH + SH * 0.1)
Y_MIN = int(SH * 0.915)
IMAGE = 'catevido.png'

# Cat position variables
x_pos = random.randrange(int(SW * 0.1), int(SW * 0.8))
y_pos = Y_MAX
is_rising = True

def main():
    global IW, IH

    # Get image, resize it to fit window
    img = Image.open(IMAGE).convert('RGBA')
    resized_img = img.resize((IW, IH))
    img = ImageTk.PhotoImage(resized_img)

    # Setting up tkinter window
    root.overrideredirect(True)
    root.wm_attributes('-transparentcolor', 'black') # ONLY WORKS ON WINDOWS
    root.config(bg='white')
    panel = Tk.Label(root, image=img)
    panel.config(bg='black')
    panel.image = img
    panel.pack()
    
    # Left / Right click event handler
    root.bind('<Button-1>', on_left_click)
    root.bind('<Button-3>', on_right_click)

    # Run the update methods and tkinter mainloop
    root.after(10, update)
    root.after(10, time_checker)
    root.mainloop()

# Window movement controller
def update():
    global y_pos 
    if is_rising and y_pos > Y_MIN:
        y_pos -= 1
    
    if not is_rising and y_pos < Y_MAX:
        y_pos += 10
    
    root.geometry('{w}x{h}+{xpos}+{ypos}'.format(w=str(IW), h=str(IH), xpos=str(x_pos), ypos=str(y_pos)))
    root.attributes('-topmost', True)

    # call update again after 30ms
    root.after(30, update)

# Checks the time and maybe a cat will appear
def time_checker():
    global x_pos
    global is_rising
    minute = datetime.now().minute
    if not is_rising:
        if random.randint(1, 7) == 7:
            is_rising = True
            x_pos = random.randrange(int(SW * 0.1), int(SW * 0.8))
    
    # call time_checker after 1min
    root.after(60000, time_checker)

# Handles left click event
def on_left_click(event):
    global is_rising 
    is_rising = False

# Handles right click event
def on_right_click(event):
    sys.exit()

# The juice
main()
