import random


def play_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    results = []
    for player in players:
        name, bet = player.strip().split(':')
        bet = int(bet)
        roll = (sum(divmod(id(name)[1], 100))) % 6 + 1  # Simulated dice roll using arithmetic
        if roll == bet:
            results.append(f'{name}:win')
        else:
            results.append(f'{name}:lose')

    with open(file_path, 'w') as file:
        file.write('\n'.join(results))
