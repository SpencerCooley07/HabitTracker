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

	def add_habit(self, name: str, description: str, created: str, habit_type: str, goal, unit, tags: list[str], streak: dict[str, float] = {"current": 0, "longest": 0}, archived: bool = False, entries: list[dict] = []):
		self.data[name] = {
			"description": description,
			"created": created,
			"habit_type": habit_type,
			"goal": goal,
			"unit": unit,
			"tags": tags,
			"streak": streak,
			"archived": archived,
			"entries": entries
		}
		self.database.save_data(self.data)

	def delete_habit(self, name: str):
		del self.data[name]
		self.database.save_data(self.data)