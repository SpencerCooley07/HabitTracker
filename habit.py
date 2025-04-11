from datetime import date

class Habit:
	def __init__(self, name: str, description: str, created: str, habit_type: str, goal: int, unit: str, tags: list[str], streak=None, entries=None) -> None:
		self.name = name
		self.description = description
		self.created = created
		self.habit_type = habit_type
		self.goal = goal
		self.unit = unit
		self.tags = tags or []
		self.streak = streak or {"current": 0, "longest": 0}
		self.entries = entries or {}