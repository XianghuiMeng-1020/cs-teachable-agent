import random


def register_entries(file_path, entries):
    with open(file_path, 'a') as f:
        for entry in entries:
            f.write(entry + '\n')


def draw_winner(file_path):
    try:
        with open(file_path, 'r') as f:
            entries = [line.strip() for line in f.readlines()]
        if entries:
            winner = random.choice(entries)
            return entries, winner
        else:
            return []
    except FileNotFoundError:
        return []