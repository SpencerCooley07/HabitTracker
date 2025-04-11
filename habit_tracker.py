from habit import Habit
from database import Database
import json
import os

class HabitTracker():
	def __init__(self) -> None:
		self.db = Database('data/database.json').load_data()
		print(self.db)
		self.habits = {}

	def add_habit(self, name: str, description: str, created: str, habit_type: str, goal: int, unit: str, tags: list[str]) -> None:
		if name not in self.db:
			self.habits[name] = Habit(name, description, created, habit_type, goal, unit, tags)

if __name__ == "__main__":
	ht = HabitTracker()