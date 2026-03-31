import random

def simulate_game(bet_number, bet_amount, probabilities):
    drawn_number = random.choices(list(probabilities.keys()), weights=list(probabilities.values()), k=1)[0]
    if drawn_number == bet_number:
        return 2 * bet_amount
    else:
        return -bet_amount