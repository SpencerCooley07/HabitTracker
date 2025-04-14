from habit_tracker import HabitTracker

import tkinter as tk
from tkinter import ttk

import sv_ttk
import darkdetect
import pywinstyles, sys

# MISC FUNCTIONS
def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000: pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def toggle_theme(root):
	sv_ttk.toggle_theme(root)
	apply_theme_to_titlebar(root)



# PROGRAM LOGIC
ht = HabitTracker()
habit_list = ht.get_habit_names()



# GUI
root = tk.Tk()

root.title("Main Window")
root.geometry("1920x1080")

habit = tk.StringVar(root, habit_list[0])
habit_select = ttk.OptionMenu(root, habit, habit_list[0], *habit_list, command= lambda value: print(f'Selected {value}'))
habit_select.place(x = 10, y = 10, height = 50, width = 400)

habit_desc = tk.Entry(root)
habit_desc.place(x=10, y=75, height = 20, width=400)


sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")
apply_theme_to_titlebar(root)
root.mainloop()