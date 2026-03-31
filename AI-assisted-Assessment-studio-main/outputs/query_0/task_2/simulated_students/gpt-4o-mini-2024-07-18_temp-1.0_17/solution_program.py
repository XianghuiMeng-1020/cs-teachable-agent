import random

def play_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()
    results = []
    for player in players:
        player_name, bet_number_str = player.strip().split(':')
        bet_number = int(bet_number_str)
        dice_roll = (sum([1 for _ in range(6)]) % 6) + 1
        result = f'{player_name}:{"win" if bet_number == dice_roll else "lose"}'
        results.append(result)
    with open(file_path, 'w') as file:
        file.write('\n'.join(results))
