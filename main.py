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

# APP
class HabitApp(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        
        # WINDOW
        # Make a fixed size window
        self.title("Habit Tracker")
        self.iconbitmap("assets/icon.ico")
        self.resizable(0,0)
        self.geometry("1920x1080")

        # LAYOUT
        self.columnconfigure(0, weight=1, minsize=640) # Initialise left column
        self.columnconfigure(1, weight=0, minsize=5) # Divider column
        self.columnconfigure(2, weight=2, minsize=1280) # Initialise right column (2x left)
        self.rowconfigure(0, weight=1)

        self.left_frame = ttk.Frame(self) # Inside the left column, set up a ttk Frame
        self.left_frame.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
        self.left_frame.columnconfigure(0, weight=1)

        self.right_frame = ttk.Frame(self) # Inside the right column, set up a ttk Frame
        self.right_frame.grid(column=2, row=0, sticky="nsew", padx=20, pady=20)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=0, minsize=5) # Scrollbar column
        self.right_frame.rowconfigure(0, weight=9)
        self.right_frame.rowconfigure(1, weight=1)

        self.divider = ttk.Separator(self, orient="vertical") # Create a divider
        self.divider.grid(column=1, row=0, sticky="ns", padx=0, pady=20) # Place in divider column

        # THEME
        sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")
        version = sys.getwindowsversion()
        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(self, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(self, "dark" if sv_ttk.get_theme() == "dark" else "normal")
            self.wm_attributes("-alpha", 0.99)
            self.wm_attributes("-alpha", 1)

        self.light_icon = tk.PhotoImage(file="assets/sun.png")
        self.dark_icon = tk.PhotoImage(file="assets/moon.png")
        self.toggle_icon = self.light_icon if sv_ttk.get_theme() == "dark" else self.dark_icon

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
        # LEFT PANEL
        # Habit Selection
        self.habit_dropdown = ttk.Combobox(self.left_frame, textvariable=self.selected_habit, state="readonly")
        self.habit_dropdown.bind("<<ComboboxSelected>>", self.update_fields)
        self.habit_dropdown.grid(column=0, row=0, padx=10, pady=10, sticky="ew")
        
        # Habit Name
        ttk.Label(self.left_frame, text="Habit Name").grid(column=0, row=1, sticky="w", padx=10, pady=(10,5))
        self.name_entry = ttk.Entry(self.left_frame, textvariable=self.name_var)
        self.name_entry.grid(column=0, row=2, sticky="ew", padx=10, pady=5)
        self.name_entry.bind("<Return>", self.save)

        # Habit Description
        ttk.Label(self.left_frame, text="Description").grid(column=0, row=3, sticky="w", padx=10, pady=(10,5))
        self.description_entry = ttk.Entry(self.left_frame, textvariable=self.description_var)
        self.description_entry.grid(column=0, row=4, sticky="ew", padx=10, pady=5)
        self.description_entry.bind("<Return>", self.save)

        # Habit Goal
        ttk.Label(self.left_frame, text="Goal").grid(column=0, row=5, sticky="w", padx=10, pady=(10,5))
        self.goal_entry = ttk.Entry(self.left_frame, textvariable=self.goal_var)
        self.goal_entry.grid(column=0, row=6, sticky="ew", padx=10, pady=5)
        self.goal_entry.bind("<Return>", self.save)

        # Habit Unit
        ttk.Label(self.left_frame, text="Unit").grid(column=0, row=7, sticky="w", padx=10, pady=(10,5))
        self.unit_entry = ttk.Entry(self.left_frame, textvariable=self.unit_var)
        self.unit_entry.grid(column=0, row=8, sticky="ew", padx=10, pady=5)
        self.unit_entry.bind("<Return>", self.save)

        # Habit Tags
        ttk.Label(self.left_frame, text="Tags").grid(column=0, row=9, sticky="w", padx=10, pady=(10,5))
        self.tags_entry = ttk.Entry(self.left_frame, textvariable=self.tags_var)
        self.tags_entry.grid(column=0, row=10, sticky="ew", padx=10, pady=5)
        self.tags_entry.bind("<Return>", self.save)

        # Save
        self.save_button = ttk.Button(self.left_frame, text="Save Changes", command=self.save)
        self.save_button.grid(column=0, row=11, sticky="ew", padx=10, pady=(20,5))

        # Delete
        self.delete_style = ttk.Style()
        self.delete_style.configure("Delete.TButton", foreground="red")

        self.delete_button = ttk.Button(self.left_frame, text="DELETE HABIT", command=self.delete)
        self.delete_button.grid(column=0, row=12, sticky="ew", padx=10, pady=5)
        self.delete_button.config(style="Delete.TButton")

        # Theme Toggle
        self.theme_button = ttk.Button(self.left_frame, image=self.toggle_icon, command=self.theme_toggle)
        self.theme_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)



        # RIGHT PANEL
        self.entries_list = ttk.Treeview(self.right_frame, columns=("date", "value", "note"), show="headings")
        self.entries_scroll = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.entries_list.yview)

        self.entries_list.heading("date", text="Date")
        self.entries_list.heading("value", text="Value")
        self.entries_list.heading("note", text="Note")
        self.entries_list.column("date", anchor="center", minwidth=120, stretch=False)
        self.entries_list.column("value", anchor="center", minwidth=120, stretch=False)
        self.entries_list.column("note", anchor="center")
        self.entries_list.config(yscrollcommand=self.entries_scroll.set)
        self.entries_list.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)
        self.entries_list.bind("<<TreeviewSelect>>", self.open_entry_editor)
        self.entries_scroll.grid(column=1, row=0, sticky="ns")
        
        self.update_dropdown()


    def theme_toggle(self) -> None:
        version = sys.getwindowsversion()
        sv_ttk.toggle_theme(self)
        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(self, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(self, "dark" if sv_ttk.get_theme() == "dark" else "normal")
            self.wm_attributes("-alpha", 0.99)
            self.wm_attributes("-alpha", 1)

        self.toggle_icon = self.light_icon if sv_ttk.get_theme() == "dark" else self.dark_icon
        self.theme_button.config(image=self.toggle_icon)

        self.delete_style.configure("Delete.TButton", foreground="red")

    def update_dropdown(self) -> None:
        habit_names = self.tracker.get_habit_names()
        self.habit_dropdown["values"] = ["Add Habit"] + habit_names

        # Get "first" habit in list if it exists
        if habit_names and not (self.selected_habit.get() or self.selected_habit.get() in habit_names): self.selected_habit.set(habit_names[0])
        elif not habit_names: self.selected_habit.set("Add Habit")
        self.update_fields()

    def update_fields(self, event=None) -> None:
        name = self.selected_habit.get()

        if name != "Add Habit":
            data = self.tracker.get_habit_data(name)

            self.name_var.set(name)
            self.description_var.set(data["description"])
            self.goal_var.set(data["goal"])
            self.unit_var.set("" if data["unit"] == None else data["unit"])
            self.tags_var.set(', '.join(data["tags"]))

        else: self.clear_fields()
        self.update_entries()

    def update_entries(self) -> None:
        name = self.selected_habit.get()
        entries = self.tracker.get_habit_entries(name)

        self.entries_list.heading("value", text=self.unit_var.get() if self.unit_var.get() else "Value")

        self.entries_list.delete(*self.entries_list.get_children())
        for i, entry in enumerate(entries): self.entries_list.insert("", "end", values=(entry["date"], entry["value"], entry["note"]))

    def clear_fields(self, event=None) -> None:
        self.name_var.set("")
        self.description_var.set("")
        self.goal_var.set("")
        self.unit_var.set("")
        self.tags_var.set("")

    def open_entry_editor(self, event=None) -> None:
        selected = self.entries_list.selection()
        if not selected: return

        entry_date, entry_value, entry_note = self.entries_list.item(selected[0], "values")

        top = tk.Toplevel(self)
        top.title('Entry Editor')
        top.iconbitmap("assets/icon.ico")
        top.resizable(0,0)
        top.geometry('400x300')

        version = sys.getwindowsversion()
        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(top, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(top, "dark" if sv_ttk.get_theme() == "dark" else "normal")
            top.wm_attributes("-alpha", 0.99)
            top.wm_attributes("-alpha", 1)

        # Date
        ttk.Label(top, text="Date").pack(pady=(10, 0))
        date_var = tk.StringVar(value=entry_date)
        date_entry = ttk.Entry(top, textvariable=date_var)
        date_entry.bind("<Return>", lambda x: save_entry())
        date_entry.pack()

        # Value
        ttk.Label(top, text="Value").pack(pady=(10, 0))
        value_var = tk.StringVar(value=entry_value)
        value_entry = ttk.Entry(top, textvariable=value_var)
        value_entry.bind("<Return>", lambda x: save_entry())
        value_entry.pack()

        # Note
        ttk.Label(top, text="Note").pack(pady=(10, 0))
        note_var = tk.StringVar(value=entry_note)
        note_entry = ttk.Entry(top, textvariable=note_var)
        note_entry.bind("<Return>", lambda x: save_entry())
        note_entry.pack()

        # Save
        def save_entry() -> None:
            new_date = date_var.get()
            new_value = value_var.get()
            new_note = note_var.get()

            if not new_value: new_value = None
            elif not new_value.replace(".", "").isnumeric() or new_value.count(".") > 1:
                messagebox.showerror("Invalid Value", "Value must be an integer or float.\nE.g. 1, 2.6, 5.7, 9")
                value_entry.config(textvariable=value_var)
                return
            else: new_value = float(new_value) if "." in new_value else int(new_value)
            
            self.tracker.habit_update_entry(self.selected_habit.get(), entry_date, new_date, new_value, new_note)

            self.update_entries()
            top.destroy()

        save_btn = ttk.Button(top, text="Save", command=save_entry)
        save_btn.pack(pady=20)

    def save(self, event=None) -> None:
        name = self.selected_habit.get()
        description = self.description_var.get().strip()
        goal = self.goal_var.get().strip()
        if goal.replace(".", "").isnumeric() and goal.count(".") <= 1: goal = float(goal) if goal.count(".") == 1 else int(goal)
        else:
            messagebox.showerror("Invalid Goal", "Goal must be an integer or float.\nE.g. 1, 2.6, 5.7, 9")
            return
        unit = self.unit_var.get().strip()
        tags = [tag.strip() for tag in self.tags_var.get().split(',')]

        if name == "Add Habit":
            self.tracker.add_habit(self.name_var.get().strip(), description, datetime.today().strftime("%Y-%m-%d"), goal, unit if unit else None, tags)
            messagebox.showinfo("Success", "Habit added successfully!")
            self.selected_habit.set(self.name_var.get().strip())
            self.update_dropdown()
            return

        if name != self.name_entry.get().strip():
            if not messagebox.askokcancel("Habit Name Change", "You are changing the name of the habit."):
                self.name_var.set(name)
                return
            if self.name_var.get().strip() in self.tracker.get_habit_names():
                messagebox.showerror("Habit Name Change", "A habit with this name already exists.")
                self.name_var.set(name)
                return

        self.tracker.habit_update_description(name, description)
        self.tracker.habit_update_goal(name, goal)
        self.tracker.habit_update_unit(name, unit)
        self.tracker.habit_update_tags(name, tags)
        self.tracker.habit_update_name(name, self.name_var.get().strip()) # Update name last to ensure other updates target correct habit

        messagebox.showinfo("Success", "Habit updated successfully!")
        self.selected_habit.set(self.name_var.get().strip())
        self.update_dropdown()

    def delete(self, event=None) -> None:
        name = self.selected_habit.get()

        if name != "Add Habit":
            if not messagebox.askokcancel("Delete Habit Confirmation", "Are you sure you wish to delete this habit?\nAll data will be lost."):
                return
            self.tracker.delete_habit(name)
            self.selected_habit.set(self.tracker.get_habit_names()[0])
            self.update_dropdown()

        else:
            if not messagebox.askokcancel("Clear Habit Properties", "Are you sure you wish to clear all habit properties?"): return
            self.clear_fields()

if __name__ == "__main__":
    app = HabitApp()
    app.mainloop()