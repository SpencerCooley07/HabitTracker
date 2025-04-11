import json
import os

class Database:
    def __init__(self, filename="data/database.json"):
        self.filename = filename
        

    def load_data(self):
        if not os.path.exists(self.filename): return {}
        with open(self.filename, "r") as file: data = json.load(file)
        return data
