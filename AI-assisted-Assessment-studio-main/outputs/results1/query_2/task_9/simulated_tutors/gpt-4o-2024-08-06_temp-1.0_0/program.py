import os
import random

def register_entries(file_path, entries):
    """
    Write player names to the given file path. If file exists, append names; otherwise, create file.
    """
    with open(file_path, 'a') as file:  # 'a' mode to append new entries
        for entry in entries:
            file.write(f"{entry}\n")

def draw_winner(file_path):
    """
    Read player names from the given file path and draw a random winner.
    Return a list of entries along with the winner's name.
    """
    entries = []
    if os.path.exists(file_path):  # Check if the file exists
        with open(file_path, 'r') as file:
            entries = file.read().strip().split('\n')
    # Return empty list if no entries
    if len(entries) == 0:
        return []
    # Randomly select a winner
    winner = random.choice(entries)
    return entries, winner