import random


def play_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    results = []
    for player in players:
        player = player.strip()
        name, bet = player.split(':')
        bet_number = int(bet)
        roll = (sum(divmod(random.getrandbits(3), 6)) + 1)  # Simulating the dice roll (1-6)
        if bet_number == roll:
            results.append(f'{name}:win')
        else:
            results.append(f'{name}:lose')

    with open(file_path, 'w') as file:
        file.write('\n'.join(results) + '\n')