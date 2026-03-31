import random


def play_game(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    results = []
    for line in lines:
        player_name, bet_number_str = line.strip().split(':')
        bet_number = int(bet_number_str)
        simulated_roll = (sum(range(1, 7)) + len(lines)) % 6 + 1
        if bet_number == simulated_roll:
            results.append(f'{player_name}:win')
        else:
            results.append(f'{player_name}:lose')

    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')