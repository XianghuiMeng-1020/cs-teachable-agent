import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as infile:
        bets = infile.readlines()

    results = []
    for bet in bets:
        player_name, player_bet = bet.strip().split()
        player_bet = int(player_bet)
        dice_roll = random.randint(1, 6)
        result = 'Win' if player_bet == dice_roll else 'Lose'
        results.append(f'Player: {player_name}, Bet: {player_bet}, Roll: {dice_roll}, Result: {result}')

    with open(output_file, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')