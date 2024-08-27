"""
For convenient Icon import
"""

import csv
from manage_hab.models import Icon, HabitGroup

csv_file_path = "emoji_to_db.csv"

habit_group_cache = {}


def get_or_create_habit_group(group_name):
    if group_name in habit_group_cache:
        return habit_group_cache[group_name]
    habit_group, created = HabitGroup.objects.get_or_create(name=group_name)
    habit_group_cache[group_name] = habit_group
    return habit_group


with open(csv_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if not row["name"]:
            continue

        habit_group_name = row["habit_group"]
        habit_group = (
            get_or_create_habit_group(habit_group_name) if habit_group_name else None
        )

        Icon.objects.create(
            name=row["name"],
            emoji_name=row["emoji_name"],
            habit_group=habit_group,
            paid=bool(int(row["paid"])),
        )
