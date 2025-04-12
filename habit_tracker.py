from datetime import date
import json
import os

class Database:
    def __init__(self, filename="data/database.json"):
        self.filename = filename
        
    def load_data(self):
        if not os.path.exists(self.filename): return {}
        with open(self.filename, "r") as file: data = json.load(file)
        return data



class HabitTracker():
	def __init__(self) -> None:
		self.db: dict = Database('data/database.json').load_data()

	def debug_display(self) -> None:
		for name, data in self.db.items(): print(f'{name}\n{data}\n')



if __name__ == "__main__":
	ht = HabitTracker()
	ht.debug_display()