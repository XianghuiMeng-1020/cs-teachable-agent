import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            player_bet = line.strip().split()
            player_name = player_bet[0]
            player_bet_number = int(player_bet[1])
            dice_roll = random.randint(1, 6)
            result = 'Win' if player_bet_number == dice_roll else 'Lose'
            outfile.write(f'Player: {player_name}, Bet: {player_bet_number}, Roll: {dice_roll}, Result: {result}\n')