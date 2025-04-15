import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
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

        # Theme icons
        self.moon_icon = tk.PhotoImage(file="assets/moon.png")
        self.sun_icon = tk.PhotoImage(file="assets/sun.png")
        self.current_icon = self.moon_icon if sv_ttk.get_theme() == "light" else self.sun_icon

        self.theme_button = ttk.Button(self.left_frame, image=self.current_icon, command=self.toggle_theme_icon)
        self.theme_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

        sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")
        apply_theme_to_titlebar(self)

    def toggle_theme_icon(self):
        toggle_theme(self)
        new_theme = sv_ttk.get_theme()
        self.current_icon = self.moon_icon if new_theme == "light" else self.sun_icon
        self.theme_button.config(image=self.current_icon)

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
        self.habit_dropdown = ttk.Combobox(self.left_frame, textvariable=self.selected_habit, state="readonly")
        self.habit_dropdown.bind("<<ComboboxSelected>>", self.update_fields_from_selection)
        self.habit_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.habit_dropdown["values"] = ["Add Habit"] + self.tracker.get_habit_names()

        ttk.Label(self.left_frame, text="Habit Name:").grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        self.name_entry = ttk.Entry(self.left_frame, textvariable=self.name_var, width=50)
        self.name_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.name_entry.bind("<Return>", self.save_changes)

        ttk.Label(self.left_frame, text="Description:").grid(row=3, column=0, sticky="w", padx=10, pady=(10, 5))
        self.description_entry = ttk.Entry(self.left_frame, textvariable=self.description_var, width=50)
        self.description_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.description_entry.bind("<Return>", self.save_changes)

        ttk.Label(self.left_frame, text="Goal:").grid(row=5, column=0, sticky="w", padx=10, pady=(10, 5))
        self.goal_entry = ttk.Entry(self.left_frame, textvariable=self.goal_var, width=50)
        self.goal_entry.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
        self.goal_entry.bind("<KeyRelease>", self.update_unit_entry_state)  # Update state on key release
        self.goal_entry.bind("<Return>", self.save_changes)

        ttk.Label(self.left_frame, text="Unit:").grid(row=7, column=0, sticky="w", padx=10, pady=(10, 5))
        self.unit_entry = ttk.Entry(self.left_frame, textvariable=self.unit_var, width=50)
        self.unit_entry.grid(row=8, column=0, padx=10, pady=5, sticky="ew")
        self.unit_entry.bind("<Return>", self.save_changes)

        ttk.Label(self.left_frame, text="Tags (comma-separated):").grid(row=9, column=0, sticky="w", padx=10, pady=(10, 5))
        self.tags_entry = ttk.Entry(self.left_frame, textvariable=self.tags_var, width=50)
        self.tags_entry.grid(row=10, column=0, padx=10, pady=5, sticky="ew")
        self.tags_entry.bind("<Return>", self.save_changes)

        self.save_button = ttk.Button(self.left_frame, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=11, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")

        # Streak Counter Frame
        self.streak_frame = ttk.Frame(self.left_frame)
        self.streak_frame.grid(row=12, column=0, padx=10, pady=(10, 20), sticky="ew")

        self.streak_current_label = ttk.Label(self.streak_frame, text="Current: 0", anchor="center")
        self.streak_current_label.grid(row=0, column=0, padx=10, pady=5)

        self.streak_longest_label = ttk.Label(self.streak_frame, text="Longest: 0", anchor="center")
        self.streak_longest_label.grid(row=1, column=0, padx=10, pady=5)

        # Create a custom style for DELETE button with red text
        style = ttk.Style()
        style.configure("DeleteButton.TButton", foreground="red")

    def update_unit_entry_state(self, event=None):
        goal_value = self.goal_var.get().strip()
        if goal_value == "True" or goal_value == "False":
            self.unit_entry.config(state="disabled")
            self.unit_var.set("")
        else:
            self.unit_entry.config(state="normal")

    def populate_dropdown(self):
        habit_names = self.tracker.get_habit_names()
        self.habit_dropdown["values"] = ["Add Habit"] + habit_names
        if habit_names:
            self.selected_habit.set(habit_names[0])
            self.update_fields_from_selection()

    def update_fields_from_selection(self, event=None):
        name = self.selected_habit.get()
        if name == "Add Habit":
            self.name_var.set("")
            self.save_button.config(text="Add Habit")
            self.description_var.set("")
            self.goal_var.set("")
            self.unit_var.set("")
            self.tags_var.set("")
            self.unit_entry.config(state="normal")
        elif name:
            data = self.tracker.get_habit_data(name)
            self.name_var.set(name)
            self.description_var.set(data["description"])
            self.goal_var.set(data["goal"])
            self.unit_var.set("" if data["unit"] is None else data["unit"])
            self.tags_var.set(", ".join(data["tags"]))
            self.save_button.config(text="Save Changes")
            self.update_unit_entry_state()

            # Get the current streak and longest streak
            current_streak, longest_streak = self.tracker.get_habit_streak(name)
            
            # Update the streak counter label with both current and longest streak
            self.streak_current_label.config(text=f"Current: {current_streak}")
            self.streak_longest_label.config(text=f"Longest: {longest_streak}")

    def save_changes(self, event=None):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Habit name cannot be empty.")
            return

        if self.save_button.cget("text") == "Add Habit":
            try:
                goal_input = self.goal_var.get().strip()
                goal = eval(goal_input)
                if not isinstance(goal, (int, float, bool)):
                    raise ValueError
            except:
                messagebox.showerror("Invalid Goal", "Goal must be a number or boolean value.\nE.g. 1, 2.6, True/False")
                return

            self.tracker.add_habit(
                name,
                self.description_var.get(),
                datetime.today().strftime("%Y-%m-%d"),
                goal,
                self.unit_var.get() if not isinstance(goal, bool) else None,
                [tag.strip() for tag in self.tags_var.get().split(',')] if self.tags_var.get().strip() else []
            )
            messagebox.showinfo("Success", "Habit added successfully!")

            self.populate_dropdown()
            self.selected_habit.set(name)
            self.update_fields_from_selection()

        else:
            self.update_habit(name)

    def update_habit(self, name):
        try:
            goal_input = self.goal_var.get().strip()
            goal = eval(goal_input)
            if not isinstance(goal, (int, float, bool)):
                raise ValueError
        except:
            messagebox.showerror("Invalid Goal", "Goal must be a number or boolean value.\nE.g. 1, 2.6, True/False")
            return

        description = self.description_var.get().strip()
        unit = self.unit_var.get().strip() or None if not isinstance(goal, bool) else None
        tags = [tag.strip() for tag in self.tags_var.get().split(",") if tag.strip()]

        self.tracker.habit_update_description(name, description)
        self.tracker.habit_update_goal(name, goal)
        self.tracker.habit_update_unit(name, unit)
        self.tracker.habit_update_tags(name, tags)

        updated_data = self.tracker.get_habit_data(name)
        self.description_var.set(updated_data["description"])
        self.goal_var.set(updated_data["goal"])
        self.unit_var.set(updated_data["unit"] if updated_data["unit"] else "")
        self.tags_var.set(", ".join(updated_data["tags"]))
        self.update_unit_entry_state(goal)

        messagebox.showinfo("Success", "Habit updated successfully!")

    def delete_habit(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "No habit selected to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the habit: '{name}'?")
        if confirm:
            self.tracker.delete_habit(name)
            messagebox.showinfo("Success", f"Habit '{name}' deleted successfully!")

            # Clear fields and update dropdown
            self.clear_fields()
            self.populate_dropdown()

    def clear_fields(self):
        self.name_var.set("")
        self.description_var.set("")
        self.goal_var.set("")
        self.unit_var.set("")
        self.tags_var.set("")

if __name__ == "__main__":
    app = HabitApp()
    app.mainloop()