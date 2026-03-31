import random


def play_game(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    results = []
    for line in lines:
        player_name, bet_number = line.strip().split(':')
        bet_number = int(bet_number)
        roll = ((random.randint(1, 6) * 3) % 6) + 1  # Simulate a dice roll
        if bet_number == roll:
            results.append(f'{player_name}:win')
        else:
            results.append(f'{player_name}:lose')
    with open(file_path, 'w') as file:
        file.write('\n'.join(results))