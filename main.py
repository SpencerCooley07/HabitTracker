import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

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
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("1920x1080")

        self.columnconfigure(0, weight=1, minsize=640)
        self.columnconfigure(1, weight=0, minsize=5)
        self.columnconfigure(2, weight=2, minsize=1280)
        self.rowconfigure(0, weight=1)

        self.tracker = HabitTracker()
        self.selected_habit = tk.StringVar()
        self.description_var = tk.StringVar()
        self.goal_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.name_var = tk.StringVar()

        self.setup_layout()
        self.populate_dropdown()

        sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")
        apply_theme_to_titlebar(self)

    def setup_layout(self):
        self.left_frame = ttk.Frame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.left_frame.columnconfigure(0, weight=1)

        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)

        self.divider = ttk.Separator(self, orient="vertical")
        self.divider.grid(row=0, column=1, sticky="ns", padx=0, pady=20)

        self.setup_widgets()

    def setup_widgets(self):

        # Dropdown to select habit
        self.habit_dropdown = ttk.Combobox(self.left_frame, textvariable=self.selected_habit, state="readonly")
        self.habit_dropdown.bind("<<ComboboxSelected>>", self.update_fields_from_selection)
        self.habit_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Habit Name
        ttk.Label(self.left_frame, text="Habit Name:").grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        self.name_entry = ttk.Entry(self.left_frame, textvariable=self.name_var, width=50)
        self.name_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.name_entry.bind("<Return>", self.save_changes)

        # Description
        ttk.Label(self.left_frame, text="Description:").grid(row=3, column=0, sticky="w", padx=10, pady=(10, 5))
        self.description_entry = ttk.Entry(self.left_frame, textvariable=self.description_var, width=50)
        self.description_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.description_entry.bind("<Return>", self.save_changes)

        # Goal
        ttk.Label(self.left_frame, text="Goal:").grid(row=5, column=0, sticky="w", padx=10, pady=(10, 5))
        self.goal_entry = ttk.Entry(self.left_frame, textvariable=self.goal_var, width=50)
        self.goal_entry.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
        self.goal_entry.bind("<Return>", self.save_changes)

        # Unit
        ttk.Label(self.left_frame, text="Unit:").grid(row=7, column=0, sticky="w", padx=10, pady=(10, 5))
        self.unit_entry = ttk.Entry(self.left_frame, textvariable=self.unit_var, width=50)
        self.unit_entry.grid(row=8, column=0, padx=10, pady=5, sticky="ew")
        self.unit_entry.bind("<Return>", self.save_changes)

        # Tags
        ttk.Label(self.left_frame, text="Tags (comma-separated):").grid(row=9, column=0, sticky="w", padx=10, pady=(10, 5))
        self.tags_entry = ttk.Entry(self.left_frame, textvariable=self.tags_var, width=50)
        self.tags_entry.grid(row=10, column=0, padx=10, pady=5, sticky="ew")
        self.tags_entry.bind("<Return>", self.save_changes)

        # Save button
        self.save_button = ttk.Button(self.left_frame, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=11, column=0, padx=10, pady=(20, 10), sticky="w")

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
            self.name_var.set(name)
            self.description_var.set(data["description"])
            self.goal_var.set(str(data["goal"]))
            self.unit_var.set("" if data["unit"] is None else data["unit"])
            self.tags_var.set(", ".join(data["tags"]))

    def save_changes(self, event=None):
        name = self.selected_habit.get()
        new_name = self.name_var.get().strip()

        if not name or not new_name: return

        if new_name != name:
            self.tracker.habit_update_name(name, new_name)
            habit_names = self.tracker.get_habit_names()
            self.habit_dropdown["values"] = habit_names
            self.selected_habit.set(new_name)
            self.update_fields_from_selection()

        try:
            goal_input = self.goal_var.get().strip()
            goal = eval(goal_input)
            if not isinstance(goal, (int, float, bool)): raise ValueError
        except:
            messagebox.showerror("Invalid Goal", "Goal must be a number or boolean value.")
            return

        description = self.description_var.get().strip()
        unit = self.unit_var.get().strip() or None
        tags = [tag.strip() for tag in self.tags_var.get().split(",") if tag.strip()]

        self.tracker.habit_update_description(new_name, description)
        self.tracker.habit_update_goal(new_name, goal)
        self.tracker.habit_update_unit(new_name, unit)
        self.tracker.habit_update_tags(new_name, tags)

        updated_data = self.tracker.get_habit_data(new_name)
        self.description_var.set(updated_data["description"])
        self.goal_var.set(str(updated_data["goal"]))
        self.unit_var.set(updated_data["unit"] if updated_data["unit"] else "")
        self.tags_var.set(", ".join(updated_data["tags"]))

        messagebox.showinfo("Success", "Habit updated successfully!")

if __name__ == "__main__":
    app = HabitApp()
    app.mainloop()