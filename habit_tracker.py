from datetime import datetime
import json
import os

class Database:
    def __init__(self, filename="data/database.json"):
        self.filename = filename
        
    def load_data(self):
        if not os.path.exists(self.filename): return {}
        with open(self.filename, "r") as file: data = json.load(file)
        return data

    def save_data(self, data):
    	if not os.path.exists(self.filename): os.mkdir(self.filename)
    	with open(self.filename, "w") as file: json.dump(data, file, indent=2)



class HabitTracker():
	def __init__(self) -> None:
		self.db = Database('data/database.json')
		self.data: dict = self.db.load_data()

	def add_habit(self, name: str, description: str, habit_type: str, goal: int, unit: str, tags: list[str]):
		self.data[name] = {
			"description": description,
			"created": datetime.today().strftime("%Y-%m-%d"),
			"last_updated": datetime.today().strftime("%Y-%m-%d"),
			"habit_type": habit_type,
			"goal": goal,
			"unit": unit,
			"tags": tags,
			"streak": { "current": 0, "longest": 0 },
			"archived": False,
			"entries": {}
		}
		self.db.save_data(self.data)


	def __repr__(self) -> str:
		output_string = f""
		for name, data in self.data.items(): output_string += f'{name}\n{data}\n\n'
		return output_string



if __name__ == "__main__":
	ht = HabitTracker()
	ht.add_habit("Water", "Drink enough water", "numeric", 3, "litres", ["health"])
	print(repr(ht))