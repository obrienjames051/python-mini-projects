import tkinter as tk #tkinter builds the GUI
from tkinter import messagebox #messagebox   shows popups
import random
from PIL import Image, ImageTk #PIL is a library developed to let you open, manipulate, and save image files
from pathlib import Path

root = tk.Tk() # tk.Tk() creates a main window. Root is the common variable name used
root.title("Dice Roller") #this sets the title of the window

window_width = 380 #size of the window
window_height = 380
screen_width = root.winfo_screenwidth() #gets the total width of the screen
screen_height = root.winfo_screenheight() #gets the total height of the screen
x = (screen_width // 2) - (window_width // 2) #calculates where to place the window
y = (screen_height // 2) - (window_height // 2) # // is integer division which avoids decimals as geometry() expects a whole number

root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # width x height in pixels + distance from left edge of screen + distance from top edge of screen
root.configure(bg="#86d7f7")  # light blue background

dice_label = (tk.Label(root, text="How many dice?", bg="#86d7f7", font=("Helvetica", 15, "bold underline"))) #this creates a label widget within root.
dice_label.grid(row=0, column=0) #.grid tells tkinter where to place it
# bg -> background colour, fg -> foreground (text) colour, font=("Font Family", size, "style") style = "bold", "underlined", "italic", or combine
entry_dice = tk.Entry(root, font=("Helvetica", 14), relief="raised", bd=2, highlightthickness=2, highlightbackground="grey") #This creates an input box
#relief changes how the edge looks, highlightthickness changes the width of the border, bd changes the gap between border and text box
entry_dice.grid(row=0, column=1, pady=10) #this tells tkinter to put the input box next to the label

same_sides_var = tk.BooleanVar() #creates a tkinter variable that stores a boolean, tracks whether the checkbox is ticked or not
same_sides_check = tk.Checkbutton(root, text="All dice have the same number of sides", bg="#86d7f7", variable=same_sides_var, wraplength=200, justify="left")
#this creates the checkbox widget, variable links to the above line, wraplength wraps to multiple lines, justify snaps to the left
same_sides_check.grid(row=1, columnspan=2) # This places the checkbox across two columns

tk.Label(root, text="Sides per die (e.g. 6 8 4):", bg="#86d7f7", font=("Helvetica", 15, "bold underline")).grid(row=2, column=0, padx=10) #This chunk is the same as two chunks above
entry_sides = tk.Entry(root, font=("Helvetica", 14), relief="raised", bd=2, highlightthickness=2, highlightbackground="grey")
entry_sides.grid(row=2, column=1, pady=10)

def roll_dice():
    try:
        num_dice = int(entry_dice.get()) # .get() is how you retrieve the current value from a tkinter widget or control
        if num_dice < 1:
            raise ValueError("Number of dice must be at least 1.") #stops the current code and jumps to the except line at the bottom of this block

        if same_sides_var.get():
            sides = int(entry_sides.get())
            if sides < 2:
                raise ValueError("Each die must have at least 2 sides.")
            dice_sides = [sides] * num_dice
        else:
            side_strings = entry_sides.get().split() #this splits the input into separate strings
            if len(side_strings) != num_dice:
                raise ValueError(f"Enter exactly {num_dice} side values.")
            dice_sides = [int(s) for s in side_strings]
            if any(s < 2 for s in dice_sides):
                raise ValueError("Each die must have at least 2 sides.")
        rolls = [random.randint(1, s) for s in dice_sides]
        result_label.config(text=f"Rolls: {rolls} | Total: {sum(rolls)}", bg="white", font=("Helvetica", 15), relief="raised", bd=4, highlightthickness=2, highlightbackground="grey") #this is a tk.Label widget. .config changes its settings, in this case the text
    except ValueError as e:
        messagebox.showerror("Input Error", str(e)) #this creates a pop-up error window, e is the message that appears

tk.Button(root, text="Roll Dice!", command=roll_dice, font=("Helvetica", 15, "bold"), relief="raised", bd=1, highlightthickness=1, highlightbackground="grey").grid(row=3, columnspan=2, pady=20) #this is the button that triggers the above code. pady=10 means leave 10 pixels of vertical space above and below the widget
#padx=10 adds horizontal padding    # command = roll_dice not roll_dice() because having the () would call the function immediately

result_label = tk.Label(root, text="", bg="#86d7f7") #this displays the result using the values worked out in the above loop
result_label.grid(row=4, columnspan=2, pady=10)

# Load the D20 image from the same folder as this script so the program works
# when launched from any working directory (helpful when sharing or uploading).
script_dir = Path(__file__).parent
img_path = script_dir / "D20.png"
try:
    d20_image = Image.open(img_path)
    # Pillow 9+ uses Image.Resampling; older versions expose LANCZOS/ANTIALIAS directly.
    try:
        resample = Image.Resampling.LANCZOS
    except Exception:
        resample = getattr(Image, 'LANCZOS', getattr(Image, 'ANTIALIAS', None))
    if resample is None:
        d20_image = d20_image.resize((100, 100))
    else:
        d20_image = d20_image.resize((100, 100), resample)
    d20_photo = ImageTk.PhotoImage(d20_image)
    image_label = tk.Label(root, image=d20_photo, bg="#86d7f7")
    image_label.image = d20_photo  # keep a reference so Tkinter doesn't garbage-collect it
except Exception as e:
    print(f"Warning: couldn't load image {img_path!s}: {e}")
    image_label = tk.Label(root, text="[D20.png missing]", bg="#86d7f7", font=("Helvetica", 12, "italic"))

image_label.grid(row=5, columnspan=2, pady=10)

root.mainloop() #this tells Python to start the GUI event loop and keeps it running/responsive