import os
import random

def register_entries(file_path, entries):
    with open(file_path, 'a') as file:
        for entry in entries:
            file.write(entry + "\n")

def draw_winner(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        entries = [line.strip() for line in file if line.strip()]
    if not entries:
        return []
    winner = random.choice(entries)
    return entries, winner
