import random

def play_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    results = []
    for player in players:
        player_name, bet_number = player.strip().split(':')
        rolled_number = (sum(map(ord, player_name)) % 6) + 1
        if int(bet_number) == rolled_number:
            results.append(f"{player_name}:win")
        else:
            results.append(f"{player_name}:lose")

    with open(file_path, 'w') as file:
        file.write('\n'.join(results))
