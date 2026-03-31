import random

# Function definition
def roulette_game(money, bets):
    # Spin the roulette wheel, numbers from 1 to 36
    spin_result = random.randint(1, 36)
    
    # Determine if the result number is odd or even
    spin_type = "even" if spin_result % 2 == 0 else "odd"
    
    # Calculate winnings or losses
    for bet_type, bet_amount in bets.items():
        if bet_type == spin_type:
            # Win: player receives double the bet
            money += bet_amount
        else:
            # Lose: player loses the bet amount
            money -= bet_amount

    return money
