import random

def process_bets(input_file, output_file):
    with open(input_file, 'r') as f:
        bets = f.readlines()
    results = []
    for bet in bets:
        player, player_bet = bet.strip().split('\s+')
        player_bet = int(player_bet)
        dice_roll = random.randint(1, 6)
        result = 'Win' if player_bet == dice_roll else 'Lose'
        results.append(f"Player: {player}, Bet: {player_bet}, Roll: {dice_roll}, Result: {result}")
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')