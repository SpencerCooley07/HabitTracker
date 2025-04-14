from habit_tracker import HabitTracker

import tkinter
from tkinter import ttk

import sv_ttk
import darkdetect
import pywinstyles, sys

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

root = tkinter.Tk()



button = ttk.Button(root, text="Click me!")
button.pack()



sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")
apply_theme_to_titlebar(root)
root.mainloop()