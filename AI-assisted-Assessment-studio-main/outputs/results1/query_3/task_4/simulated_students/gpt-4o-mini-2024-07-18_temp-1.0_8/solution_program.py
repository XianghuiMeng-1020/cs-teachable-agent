import random

def simulate_game(bet_number, bet_amount, probabilities):
    # Draw a number according to the specified probabilities
    drawn_number = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    
    # Determine if the player wins or loses
    if drawn_number == bet_number:
        return bet_amount * 2  # Win condition (double the bet)
    else:
        return -bet_amount  # Lose condition (lose the bet amount)