import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as infile:
        bets = infile.readlines()

    results = []
    for bet in bets:
        bet = bet.strip()
        player_name, player_bet = bet.split()
        player_bet = int(player_bet)
        dice_roll = random.randint(1, 6)
        result = 'Win' if player_bet == dice_roll else 'Lose'
        results.append(f'Player: {player_name}, Bet: {player_bet}, Roll: {dice_roll}, Result: {result}')

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(results) + '\n')