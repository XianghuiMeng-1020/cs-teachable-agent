import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as file:
        bets = file.readlines()

    results = []
    for line in bets:
        name, bet = line.strip().split()
        bet = int(bet)
        roll = random.randint(1, 6)
        result = 'Win' if roll == bet else 'Lose'
        results.append(f'Player: {name}, Bet: {bet}, Roll: {roll}, Result: {result}')

    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')