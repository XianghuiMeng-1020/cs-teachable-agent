import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as infile:
        bets = infile.readlines()

    results = []
    for bet in bets:
        name, player_bet = bet.strip().split()  # Split the line into name and bet
        player_bet = int(player_bet)  # Convert the bet to an integer
        dice_roll = random.randint(1, 6)  # Simulate the dice roll
        result = 'Win' if player_bet == dice_roll else 'Lose'  # Determine win or lose
        results.append(f'Player: {name}, Bet: {player_bet}, Roll: {dice_roll}, Result: {result}')  # Format the result

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(results))  # Write all results to the output file