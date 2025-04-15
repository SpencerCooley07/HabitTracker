from datetime import datetime
import json
from nt import error
import os


class Database:
	def __init__(self, filename="data/database.json") -> None:
		self.filename = filename
		if not os.path.exists(self.filename): raise error(FileExistsError)
	
	def load_data(self) -> dict:
		with open(self.filename, "r") as file: data = json.load(file)
		return data

	def save_data(self, data) -> None:
		with open(self.filename, "w") as file: json.dump(data, file, indent=2)

class HabitTracker:
	def __init__(self) -> None:
		self.database = Database("data/database.json")
		self.data = self.database.load_data()

	def add_habit(self, name: str, description: str, created: str, goal: int | float | bool, unit: str | None, tags: list[str], streak: dict[str, float] | None = None, archived: bool = False, entries: list[dict] | None = None) -> None:
		self.data[name] = {
			"description": description,
			"created": created,
			"habit_type": "bool" if (type(goal) == bool) else "numeric",
			"goal": goal,
			"unit": unit,
			"tags": sorted(tags, key=str.lower),
			"streak": {"current": 0, "longest": 0} if streak == None else streak,
			"archived": archived,
			"entries": [] if entries == None else entries
		}
		self.data = dict(sorted(self.data.items()))
		self.database.save_data(self.data)

	def delete_habit(self, name: str) -> None:
		del self.data[name]
		self.database.save_data(self.data)

	def habit_add_entry(self, name: str, date: str, value: int | float | bool, note: str = "") -> None:
		entries = self.data[name]["entries"]

		if (type(value) == int or float) and (self.data[name]["habit_type"] == "bool"): return
		if (type(value) == bool) and (self.data[name]["habit_type"] == "numeric"): return
		
		for i, entry in enumerate(entries):
			if date < entry["date"]:
				entries.insert(i, {"date": date, "value": value, "note": note})
				self.habit_update_streak(name)
				return

		entries.append({"date": date, "value": value, "note": note})
		self.habit_update_streak(name)

	def habit_del_entry(self, name: str, date: str) -> None:
		entries = self.data[name]["entries"]

		for i, entry in enumerate(entries):
			if date == entry["date"]:
				del entries[i]

		self.habit_update_streak(name)

	def habit_update_streak(self, name: str) -> None:
		entries = self.data[name]["entries"]
		dates = [datetime.strptime(entry["date"], "%Y-%m-%d").toordinal() for entry in entries]
		current_streak, longest_streak = 1, 1
		for i in range(1, len(dates)):
			if dates[i] - dates[i-1] == 1: current_streak += 1
			else:
				longest_streak = max(current_streak, longest_streak)
				current_streak = 1

		self.data[name]["streak"] = {"current": current_streak, "longest": max(current_streak, longest_streak)}
		self.database.save_data(self.data)

	def habit_update_name(self, name: str, new_name: str) -> None:
		self.data[new_name] = self.data.pop(name)
		self.data = dict(sorted(self.data.items()))
		self.database.save_data(self.data)

	def habit_update_description(self, name: str, new_description: str) -> None:
		self.data[name]["description"] = new_description
		self.database.save_data(self.data)

	def habit_update_goal(self, name: str, new_goal: int | float | bool) -> None:
		old_goal = self.data[name]["goal"]
		self.data[name]["goal"] = new_goal
		if (type(old_goal) == int or float) and (type(new_goal) == bool): self.data[name]["entries"].clear()
		if (type(old_goal) == bool) and (type(new_goal) == int or float): self.data[name]["entries"].clear()

		if type(new_goal) == bool:
			self.data[name]["habit_type"] = "bool"
			self.habit_update_unit(name, None)
			return

		self.data[name]["habit_type"] = "numeric"
		self.database.save_data(self.data)

	def habit_update_unit(self, name: str, new_unit: str | None) -> None:
		self.data[name]["unit"] = new_unit
		self.database.save_data(self.data)

	def habit_update_tags(self, name: str, new_tags: list[str]) -> None:
		self.data[name]["tags"] = sorted(new_tags, key=str.lower)
		self.database.save_data(self.data)

	def habit_add_tags(self, name: str, new_tags: list[str]) -> None:
		self.data[name]["tags"] += new_tags
		self.data[name]["tags"].sort(key=str.lower)
		self.database.save_data(self.data)

	def habit_del_tags(self, name: str, tag: str) -> None:
		self.data[name]["tags"].remove(tag)
		self.database.save_data(self.data)

	def habit_toggle_archive(self, name: str) -> None:
		self.data[name]["archived"] = not self.data[name]["archived"]
		self.database.save_data(self.data)

	def get_habit_data(self, name: str) -> dict: return self.data[name]

	def get_habit_names(self) -> list:
		return [name for name in self.data.keys()]