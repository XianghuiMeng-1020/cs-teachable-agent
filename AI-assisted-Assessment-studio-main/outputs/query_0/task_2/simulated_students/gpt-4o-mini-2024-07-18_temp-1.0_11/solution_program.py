import random

def play_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    results = []
    for player in players:
        player_name, bet_number = player.strip().split(':')
        bet_number = int(bet_number)
        simulated_roll = (random.randint(1, 6))

        if bet_number == simulated_roll:
            results.append(f'{player_name}:win')
        else:
            results.append(f'{player_name}:lose')

    with open(file_path, 'w') as file:
        file.write('\n'.join(results))
