from datetime import datetime, timedelta
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
		- Delete entries
		- Calculate streaks
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
		date_today = datetime.today().strftime("%Y-%m-%d")

		for i, entry in enumerate(self.entries):
			if entry["date"] > date:
				self.entries.insert(i, {"date": date, "value": value})
				if date_today == date and datetime.strptime(date, "%Y-%m-%d").toordinal() - datetime.strptime(self.entries[-2]["date"], "%Y-%m-%d").toordinal() == 1:
					self.streak["current"] += 1
					self.streak["longest"] = max(self.streak["current"], self.streak["longest"])
					return
				self.update_streak()
				return

		self.entries.append({"date": date, "value": value})
		if date_today == date and datetime.strptime(date, "%Y-%m-%d").toordinal() - datetime.strptime(self.entries[-2]["date"], "%Y-%m-%d").toordinal() == 1:
			self.streak["current"] += 1
			self.streak["longest"] = max(self.streak["current"], self.streak["longest"])
			return
		self.update_streak()

	def delete_entry(self, date: str) -> None:
		for i, entry in enumerate(self.entries):
			if entry["date"] == date:
				self.entries.pop(i)
				return

	def update_streak(self) -> None:
		dates = [datetime.strptime(entry["date"], "%Y-%m-%d").toordinal() for entry in self.entries]
		current_streak = 1
		longest_streak = 1
		for i in range(1, len(dates)):
			if dates[i] - dates[i-1] == 1:
				current_streak += 1
			else:
				longest_streak = max(current_streak, longest_streak)
				current_streak = 1

		self.streak = {"current": current_streak, "longest": max(current_streak, longest_streak)}



if __name__ == "__main__":
	# EXAMPLE DATABASE CODE
	# habit_database = Database()
	# habit_database.save_data(habit_database.load_data())

	# EXAMPLE HABIT CODE
	running = Habit("Running", "Run 1km a day", datetime.today().strftime("%Y-%m-%d"), "numeric", 1, "km", ["Health", "Fitness"])
	running.add_entry("2025-04-11", 1.01)
	running.add_entry("2025-04-10", 1.1)
	running.add_entry("2025-04-09", 2.5)
	running.add_entry("2025-04-13", 2.27)
	running.add_entry("2025-04-12", 2.1)

	print(running.streak)