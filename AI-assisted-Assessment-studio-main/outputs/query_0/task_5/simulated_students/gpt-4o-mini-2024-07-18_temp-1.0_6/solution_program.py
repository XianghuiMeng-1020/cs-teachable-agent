import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as infile:
        bets = infile.readlines()
    results = []
    for bet in bets:
        name, player_bet = bet.strip().split()
        player_bet = int(player_bet)
        roll = random.randint(1, 6)
        result = "Win" if roll == player_bet else "Lose"
        results.append(f"Player: {name}, Bet: {player_bet}, Roll: {roll}, Result: {result}")
    with open(output_file, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')