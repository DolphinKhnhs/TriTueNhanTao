from UI import UI
from Algorithm import Algorithm
import tkinter as tk


window = tk.Tk()
target= Algorithm.create_target()
UI(window, Algorithm, target)
UI.drawtable(UI.canvas_right(window), target)
window.mainloop()


