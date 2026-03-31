import random


def process_bets(input_file, output_file):
    with open(input_file, 'r') as f:
        bets = f.readlines()

    results = []
    for bet in bets:
        player_name, player_bet = bet.strip().split()  # Split the line into player and bet
        player_bet = int(player_bet)  # Convert the bet to integer
        dice_roll = random.randint(1, 6)  # Simulate the dice roll
        if player_bet == dice_roll:
            result = 'Win'
        else:
            result = 'Lose'
        results.append(f'Player: {player_name}, Bet: {player_bet}, Roll: {dice_roll}, Result: {result}')

    with open(output_file, 'w') as f:
        f.write('\n'.join(results) + '\n')