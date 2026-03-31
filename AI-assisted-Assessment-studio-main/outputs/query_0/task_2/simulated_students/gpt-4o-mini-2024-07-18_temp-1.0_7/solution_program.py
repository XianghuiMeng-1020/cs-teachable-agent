import random

def play_game(file_path):
    with open(file_path, 'r') as infile:
        players = infile.readlines()

    results = []
    for player in players:
        name, bet = player.strip().split(':')
        bet_number = int(bet)
        # Simulate a dice roll (1-6)
        roll = (random.randint(0, 5) + 1)
        if roll == bet_number:
            results.append(f'{name}:win')
        else:
            results.append(f'{name}:lose')

    with open(file_path, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')