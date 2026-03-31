import random


def register_entries(file_path, entries):
    with open(file_path, 'a') as file:
        for entry in entries:
            file.write(entry + '\n')


def draw_winner(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.read().strip().split('\n')
            if not lines:
                return []
            winner = random.choice(lines)
            return lines, winner
    except FileNotFoundError:
        return []