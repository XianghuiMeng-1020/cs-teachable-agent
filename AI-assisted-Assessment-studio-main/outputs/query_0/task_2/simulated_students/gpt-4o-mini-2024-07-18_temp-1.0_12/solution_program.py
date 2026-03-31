import random

def play_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    results = []
    for player in players:
        name, bet = player.strip().split(':')
        bet = int(bet)
        simulated_roll = (random.randint(1, 6))
        if bet == simulated_roll:
            results.append(f'{name}:win')
        else:
            results.append(f'{name}:lose')

    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')
