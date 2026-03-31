import random

def register_entries(file_path, entries):
    with open(file_path, 'a') as file:
        for entry in entries:
            file.write(entry + '\n')


def draw_winner(file_path):
    try:
        with open(file_path, 'r') as file:
            all_entries = file.read().splitlines()
            if all_entries:
                winner = random.choice(all_entries)
                return all_entries, winner
            else:
                return []
    except FileNotFoundError:
        return []