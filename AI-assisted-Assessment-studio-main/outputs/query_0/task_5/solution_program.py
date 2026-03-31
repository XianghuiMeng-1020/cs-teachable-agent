import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as f:
        bets = f.readlines()
    with open(output_file, 'w') as results:
        for bet in bets:
            player_data = bet.split()
            player_name = player_data[0]
            player_bet = int(player_data[1])
            roll = random.randint(1, 6)
            if player_bet == roll:
                outcome = 'Win'
            else:
                outcome = 'Lose'
            results.write(f'Player: {player_name}, Bet: {player_bet}, Roll: {roll}, Result: {outcome}\n')