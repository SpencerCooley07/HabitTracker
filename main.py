import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sys
from typing import Collection

import darkdetect
import pywinstyles
import sv_ttk

from habit_tracker import HabitTracker

# MISC FUNCTIONS
def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()
    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def toggle_theme(root):
    sv_ttk.toggle_theme(root)
    apply_theme_to_titlebar(root)

# APP
class HabitApp(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        
        # WINDOW
        # Make a fixed size window
        self.title("Habit Tracker")
        self.resizable(0,0)
        self.geometry("1920x1080")



        # LAYOUT
        # Initialise 3 columns where the right column is 2x as large as the left (1:2)
        self.columnconfigure(0, weight=1, minsize=640)
        self.columnconfigure(1, weight=0, minsize=5) # Divider column
        self.columnconfigure(2, weight=2, minsize=1280)
        self.rowconfigure(0, weight=1)

        # Inside the left column, set up a ttk Frame
        self.left_frame = ttk.Frame(self)
        self.left_frame.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
        self.left_frame.columnconfigure(0, weight=1)

        # Inside the right column, set up a ttk Frame
        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(column=2, row=0, sticky="nsew", padx=20, pady=20)
        self.right_frame.columnconfigure(0, weight=1)

        # Create a divider in the designated Column 1
        self.divider = ttk.Separator(self, orient="vertical")
        self.divider.grid(column=1, row=0, sticky="ns", padx=0, pady=20)



        # THEME
        sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")
        apply_theme_to_titlebar(self)

        self.light_icon = tk.PhotoImage(file="assets/sun.png")
        self.dark_icon = tk.PhotoImage(file="assets/moon.png")



        # VARS
        self.tracker = HabitTracker()
        self.selected_habit = tk.StringVar()
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.goal_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.tags_var = tk.StringVar()

        self.init_widgets()

    def init_widgets(self) -> None:
        # Habit Selection
        self.habit_dropdown = ttk.Combobox(self.left_frame, textvariable=self.selected_habit, state="readonly")
        self.habit_dropdown.bind("<<ComboboxSelected>>", self.update_fields)
        self.habit_dropdown.grid(column=0, row=0, padx=10, pady=10, sticky="ew")
        self.update_dropdown()
        
        # Habit Name
        ttk.Label(self.left_frame, text="Habit Name").grid(column=0, row=1, sticky="w", padx=10, pady=(10,5))
        self.name_entry = ttk.Entry(self.left_frame, textvariable=self.name_var)
        self.name_entry.grid(column=0, row=2, sticky="ew", padx=10, pady=5)

        # Habit Description
        ttk.Label(self.left_frame, text="Description").grid(column=0, row=3, sticky="w", padx=10, pady=(10,5))
        self.description_entry = ttk.Entry(self.left_frame, textvariable=self.description_var)
        self.description_entry.grid(column=0, row=4, sticky="ew", padx=10, pady=5)

        # Habit Goal
        ttk.Label(self.left_frame, text="Goal").grid(column=0, row=5, sticky="w", padx=10, pady=(10,5))
        self.goal_entry = ttk.Entry(self.left_frame, textvariable=self.goal_var)
        self.goal_entry.grid(column=0, row=6, sticky="ew", padx=10, pady=5)

        # Habit Unit
        ttk.Label(self.left_frame, text="Unit").grid(column=0, row=7, sticky="w", padx=10, pady=(10,5))
        self.unit_entry = ttk.Entry(self.left_frame, textvariable=self.unit_var)
        self.unit_entry.grid(column=0, row=8, sticky="ew", padx=10, pady=5)

        # Habit Tags
        ttk.Label(self.left_frame, text="Unit").grid(column=0, row=9, sticky="w", padx=10, pady=(10,5))
        self.tags_entry = ttk.Entry(self.left_frame, textvariable=self.tags_var)
        self.tags_entry.grid(column=0, row=10, sticky="ew", padx=10, pady=5)

        # Save
        self.save_button = ttk.Button(self.left_frame, text="Save Changes")
        self.save_button.grid(column=0, row=11, sticky="ew", padx=10, pady=(20,5))

        # Delete
        self.delete_style = ttk.Style()
        self.delete_style.configure("Delete.TButton", foreground="red")

        self.delete_button = ttk.Button(self.left_frame, text="DELETE HABIT", command=self.delete)
        self.delete_button.grid(column=0, row=12, sticky="ew", padx=10, pady=5)
        self.delete_button.config(style="Delete.TButton")

    def update_dropdown(self) -> None:
        habit_names = self.tracker.get_habit_names()
        self.habit_dropdown["values"] = ["Add Habit"] + habit_names

        # Get "first" habit in list if it exists
        if habit_names: self.selected_habit.set(habit_names[0])
        else: self.selected_habit.set("Add Habit")
        self.update_fields()

    def update_fields(self, event=None) -> None:
        name = self.selected_habit.get()

        if name != "Add Habit":
            data = self.tracker.get_habit_data(name)

            self.name_var.set(name)
            self.description_var.set(data["description"])
            self.goal_var.set(data["goal"])
            self.unit_var.set(data["unit"])
            self.tags_var.set(', '.join(data["tags"]))

        else: self.clear_fields()

    def clear_fields(self, event=None) -> None:
        self.name_var.set("")
        self.description_var.set("")
        self.goal_var.set("")
        self.unit_var.set("")
        self.tags_var.set("")

    def delete(self, event=None) -> None:
        name = self.selected_habit.get()

        if name != "Add Habit":
            if not messagebox.askokcancel("Delete Habit Confirmation", "Are you sure you wish to delete this habit?\nAll data will be lost."):
                return
            self.tracker.delete_habit(name)
            self.update_dropdown()

        else:
            if not messagebox.askokcancel("Clear Habit Properties", "Are you sure you wish to clear all habit properties?"): return
            self.clear_fields()




if __name__ == "__main__":
    app = HabitApp()
    app.mainloop()