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
		Can insert/delete entries, calculate streaks, update description and goal, add/update tags, and archive
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
		insert_flag = False

		for i, entry in enumerate(self.entries):
			if date < entry["date"]:
				self.entries.insert(i, {"date": date, "value": value})
				insert_flag = True
				break

		if not insert_flag: self.entries.append({"date": date, "value": value})
		if date_today == date and datetime.strptime(date, "%Y-%m-%d").toordinal() - datetime.strptime(self.entries[-2]["date"], "%Y-%m-%d").toordinal() == 1:
			self.streak["current"] += 1
			self.streak["longest"] = max(self.streak["current"], self.streak["longest"])
		else: self.update_streak()

	def delete_entry(self, date: str) -> None:
		for i, entry in enumerate(self.entries):
			if entry["date"] == date:
				self.entries.pop(i)
				return

	def update_streak(self) -> None:
		dates = [datetime.strptime(entry["date"], "%Y-%m-%d").toordinal() for entry in self.entries]
		current_streak, longest_streak = 1, 1

		for i in range(1, len(dates)):
			if dates[i] - dates[i-1] == 1: current_streak += 1
			else:
				longest_streak = max(current_streak, longest_streak)
				current_streak = 1

		self.streak = {"current": current_streak, "longest": max(current_streak, longest_streak)}

	def update_description(self, new_description: str) -> None: self.description = new_description

	def update_goal(self, new_goal: float) -> None: self.goal = new_goal

	def update_tags(self, new_tags: list[str]) -> None: self.tags = new_tags

	def add_tags(self, new_tags: list[str]) -> None: self.tags += new_tags

	def archive(self) -> None: self.archived = True

class HabitTracker:
	def __init__(self) -> None:
		"""
		- Loads DB and converts to Habit objects
		- Add habits
		x Delete habits
		x Get habit
		"""
		self.db = Database("data/database.json")
		# print(self.db.load_data())
		self.data = {key: Habit(key, value["description"], value["created"], value["habit_type"], value["goal"], value["unit"], value["tags"], value["streak"], value["archived"], value["entries"]) for key, value in self.db.load_data().items()}
		# print(self.data)

	def add_habit(self, name: str, description: str, created: str, habit_type: str, goal: float, unit: str, tags: list[str]):
		self.data[name] = Habit(name, description, created, habit_type, goal, unit, tags)
		self.save_data()
	
	def save_data(self): self.db.save_data({value.__dict__.pop('name'): value.__dict__ for value in self.data.values()})



if __name__ == "__main__":
	habit_tracker = HabitTracker()
	habit_tracker.add_habit("Water", "Drink healthy amount of water", "2025-04-2025", "numeric", 2.6, "L", ["Health"])