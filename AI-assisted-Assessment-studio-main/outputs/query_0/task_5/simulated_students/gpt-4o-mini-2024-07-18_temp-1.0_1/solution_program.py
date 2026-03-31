import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as file:
        bets = file.readlines()

    results = []
    for bet in bets:
        player_name, player_bet = bet.strip().split()
        player_bet = int(player_bet)
        dice_roll = random.randint(1, 6)
        if player_bet == dice_roll:
            result = 'Win'
        else:
            result = 'Lose'
        results.append(f'Player: {player_name}, Bet: {player_bet}, Roll: {dice_roll}, Result: {result}')

    with open(output_file, 'w') as file:
        for line in results:
            file.write(line + '\n')