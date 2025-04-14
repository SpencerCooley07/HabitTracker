from habit_tracker import HabitTracker

main = HabitTracker()
main.add_habit("Running", "Run a kilometre a day", "2025-04-1", "numeric", 1, "km", ["Health", "Fitness", "Cardio"])
main.add_habit("Journal", "Journal every night", "2025-04-1", "bool", True, None, ["Health", "Fitness", "Cardio"])
main.habit_add_entry("Running", "2025-04-13", 2.27)
main.habit_add_entry("Running", "2025-04-14", 2.56)
# main.habit_del_entry("Running", "2025-04-13")
main.habit_add_entry("Journal", "2025-04-14", True)