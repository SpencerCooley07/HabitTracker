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

	def add_habit(self, name: str, description: str, created: str, habit_type: str, goal: int | float | bool, unit: str | None, tags: list[str], streak: dict[str, float] | None = None, archived: bool = False, entries: list[dict] | None = None) -> None:
		self.data[name] = {
			"description": description,
			"created": created,
			"habit_type": habit_type,
			"goal": goal,
			"unit": unit,
			"tags": tags,
			"streak": {"current": 0, "longest": 0} if streak == None else streak,
			"archived": archived,
			"entries": [] if entries == None else entries
		}
		self.database.save_data(self.data)

	def delete_habit(self, name: str) -> None:
		del self.data[name]
		self.database.save_data(self.data)

	def habit_add_entry(self, name: str, date: str, value: int | float | bool, note: str = "") -> None:
		entries = self.data[name]["entries"]
		
		for i, entry in enumerate(entries):
			if date < entry["date"]:
				entries.insert(i, {"date": date, "value": value, "note": note})
				self.database.save_data(self.data)
				return

		entries.append({"date": date, "value": value, "note": note})
		self.database.save_data(self.data)

	def habit_del_entry(self, name: str, date: str) -> None:
		entries = self.data[name]["entries"]

		for i, entry in enumerate(entries):
			if date == entry["date"]:
				del entries[i]

		self.database.save_data(self.data)