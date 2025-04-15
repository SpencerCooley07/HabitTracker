import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

import darkdetect
import pywinstyles
import sv_ttk

from habit_tracker import HabitTracker  # assuming your backend is saved as habit_tracker.py

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

class HabitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("600x400")

        self.tracker = HabitTracker()
        self.selected_habit = tk.StringVar()
        self.description_var = tk.StringVar()
        self.goal_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.tags_var = tk.StringVar()

        self.setup_widgets()
        self.populate_dropdown()

        sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")
        apply_theme_to_titlebar(self)

    def setup_widgets(self):
        # Dropdown to select habit
        self.habit_dropdown = ttk.Combobox(self, textvariable=self.selected_habit, state="readonly")
        self.habit_dropdown.bind("<<ComboboxSelected>>", self.update_fields_from_selection)
        self.habit_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Description
        ttk.Label(self, text="Description:").grid(row=1, column=0, sticky="w", padx=10)
        self.description_entry = ttk.Entry(self, textvariable=self.description_var, width=50)
        self.description_entry.grid(row=2, column=0, padx=10, sticky="w")

        # Goal
        ttk.Label(self, text="Goal:").grid(row=3, column=0, sticky="w", padx=10)
        self.goal_entry = ttk.Entry(self, textvariable=self.goal_var, width=50)
        self.goal_entry.grid(row=4, column=0, padx=10, sticky="w")

        # Unit
        ttk.Label(self, text="Unit:").grid(row=5, column=0, sticky="w", padx=10)
        self.unit_entry = ttk.Entry(self, textvariable=self.unit_var, width=50)
        self.unit_entry.grid(row=6, column=0, padx=10, sticky="w")

        # Tags
        ttk.Label(self, text="Tags (comma-separated):").grid(row=7, column=0, sticky="w", padx=10)
        self.tags_entry = ttk.Entry(self, textvariable=self.tags_var, width=50)
        self.tags_entry.grid(row=8, column=0, padx=10, sticky="w")

        # Save button
        self.save_button = ttk.Button(self, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=9, column=0, padx=10, pady=10, sticky="w")

    def populate_dropdown(self):
        habit_names = self.tracker.get_habit_names()
        self.habit_dropdown["values"] = habit_names
        if habit_names:
            self.selected_habit.set(habit_names[0])
            self.update_fields_from_selection()

    def update_fields_from_selection(self, event=None):
        name = self.selected_habit.get()
        if name:
            data = self.tracker.get_habit_data(name)
            self.description_var.set(data["description"])
            self.goal_var.set(str(data["goal"]))
            self.unit_var.set("" if data["unit"] is None else data["unit"])
            self.tags_var.set(", ".join(data["tags"]))

    def save_changes(self):
        name = self.selected_habit.get()
        if not name:
            return

        try:
            goal_input = self.goal_var.get().strip()
            goal = eval(goal_input)
            if not isinstance(goal, (int, float, bool)):
                raise ValueError
        except:
            messagebox.showerror("Invalid Goal", "Goal must be a number or boolean value.")
            return

        description = self.description_var.get().strip()
        unit = self.unit_var.get().strip() or None
        tags = [tag.strip() for tag in self.tags_var.get().split(",") if tag.strip()]

        self.tracker.habit_update_description(name, description)
        self.tracker.habit_update_goal(name, goal)
        self.tracker.habit_update_unit(name, unit)
        self.tracker.habit_update_tags(name, tags)

        updated_data = self.tracker.get_habit_data(name)
        self.description_var.set(updated_data["description"])
        self.goal_var.set(str(updated_data["goal"]))
        self.unit_var.set(updated_data["unit"] if updated_data["unit"] else "")
        self.tags_var.set(", ".join(updated_data["tags"]))

        messagebox.showinfo("Success", "Habit updated successfully!")

if __name__ == "__main__":
    app = HabitApp()
    app.mainloop()