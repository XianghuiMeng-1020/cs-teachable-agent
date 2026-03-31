import random

def simulate_game(bet_number, bet_amount, probabilities):
    # Randomly draw a number based on the specified probabilities
    drawn_number = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    
    # Determine the result based on the drawn number
    if drawn_number == bet_number:
        return bet_amount * 2  # Win: gain twice the bet amount
    else:
        return -bet_amount  # Lose: lose the bet amount