from datetime import datetime
import json
from nt import error
import os



class Database:
	def __init__(self, filename="data/database.json") -> None:
		"""
		Database class for interacting with local JSON database
		"""

		self.filename = filename
		if not os.path.exists(self.filename): raise error(FileExistsError)
	
	def load_data(self) -> dict:
		with open(self.filename, "r") as file: data = json.load(file)
		return data

	def save_data(self, data) -> None:
		with open(self.filename, "w") as file: json.dump(data, file, indent=2)

class Habit:
	def __init__(self, name: str, description: str, created: str, habit_type: str, goal: float, unit: str, tags: list[str], streak: dict[str, float] = {"current": 0, "longest": 0}, archived: bool = False, entries: list[dict] = []) -> None:
		"""
		Habit class to:
		- Insert entries
		x Delete entries
		x Calculate streaks
		x Update description
		x Update goal
		x Update tags
		x Archive
		"""
		self.name: str = name
		self.description: str = description
		self.created: str = created
		self.habit_type: str = habit_type
		self.goal: float = goal
		self.unit: str = unit
		self.tags: list[str] = tags
		self.streak: dict[str, float] = streak
		self.archived: bool = archived
		self.entries: list[dict] = entries

	def add_entry(self, date: str, value: float) -> None:
		for i, entry in enumerate(self.entries):
			if entry["date"] < date:
				self.entries.insert(i, {"date": date, "value": value})
				return
		self.entries.append({"date": date, "value": value})

	def delete_entry(self, date: str) -> None:
		for i, entry in enumerate(self.entries):
			if entry["date"] == date:
				self.entries.pop(i)
				return



if __name__ == "__main__":
	# EXAMPLE DATABASE CODE
	# habit_database = Database()
	# habit_database.save_data(habit_database.load_data())

	# EXAMPLE HABIT CODE
	running = Habit("Running", "Run 1km a day", datetime.today().strftime("%Y-%m-%d"), "numeric", 1, "km", ["Health", "Fitness"])
	print(running.entries)
	running.add_entry("2025-04-13", 2.27)
	print(running.entries)
	running.add_entry("2025-04-12", 1.3)
	print(running.entries)
	running.add_entry("2025-04-11", 1.01)
	print(running.entries)
	running.delete_entry("2025-04-13")
	print(running.entries)