import random

def register_entries(file_path, entries):
    with open(file_path, 'a') as file:
        for entry in entries:
            file.write(entry + '\n')


def draw_winner(file_path):
    try:
        with open(file_path, 'r') as file:
            entries = [line.strip() for line in file if line.strip()]
            if entries:
                winner = random.choice(entries)
                return (entries, winner)
            return []
    except FileNotFoundError:
        return []