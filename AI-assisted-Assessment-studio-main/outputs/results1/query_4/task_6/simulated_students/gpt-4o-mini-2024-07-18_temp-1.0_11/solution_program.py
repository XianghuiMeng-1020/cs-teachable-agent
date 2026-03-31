import random

def roulette_game(money, bets):
    # Spin the roulette wheel, which results in a number between 1 and 36
    spin_result = random.randint(1, 36)
    
    # Check if the result is even or odd
    is_even = (spin_result % 2 == 0)
    
    # Update the player's money based on the bets
    for bet_type, bet_amount in bets.items():
        if bet_amount > 0:
            if bet_type == "even" and is_even:
                money += bet_amount  # Win: receive 2x the bet amount
            elif bet_type == "even":
                money -= bet_amount  # Lose: lose the bet amount
            elif bet_type == "odd" and not is_even:
                money += bet_amount  # Win: receive 2x the bet amount
            elif bet_type == "odd":
                money -= bet_amount  # Lose: lose the bet amount
    
    return money