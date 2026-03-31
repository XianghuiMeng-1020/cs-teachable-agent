import random

def simulate_game(bet_number, bet_amount, probabilities):
    draw = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]
    if draw == bet_number:
        return bet_amount * 2
    else:
        return -bet_amount