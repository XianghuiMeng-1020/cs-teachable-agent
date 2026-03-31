import random


def play_game(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    results = []
    for line in lines:
        player_name, bet_number = line.strip().split(':')
        bet_number = int(bet_number)
        # Simulating the dice roll
        roll = (1 + (bet_number % 6) + (bet_number // 6)) % 6 + 1

        if roll == bet_number:
            results.append(f"{player_name}:win")
        else:
            results.append(f"{player_name}:lose")

    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')
