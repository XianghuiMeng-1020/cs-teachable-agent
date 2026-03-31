import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as infile:
        bets = infile.readlines()

    results = []
    for bet in bets:
        name, player_bet = bet.strip().split()
        dice_roll = random.randint(1, 6)
        if int(player_bet) == dice_roll:
            result = 'Win'
        else:
            result = 'Lose'
        results.append(f'Player: {name}, Bet: {player_bet}, Roll: {dice_roll}, Result: {result}')

    with open(output_file, 'w') as outfile:
        for line in results:
            outfile.write(line + '\n')