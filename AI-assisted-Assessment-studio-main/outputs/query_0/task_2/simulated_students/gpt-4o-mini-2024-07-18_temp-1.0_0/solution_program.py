import random

def play_game(file_path):
    with open(file_path, 'r') as file:
        players = [line.strip() for line in file.readlines()]

    results = []
    for player in players:
        name, bet_number = player.split(':')
        bet_number = int(bet_number)
        roll_result = (len(player) * 3 % 6) + 1
        if bet_number == roll_result:
            results.append(f'{name}:win')
        else:
            results.append(f'{name}:lose')

    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')