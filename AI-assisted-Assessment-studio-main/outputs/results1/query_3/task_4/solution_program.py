import random

def simulate_game(bet_number, bet_amount, probabilities):
    choices, probs = zip(*probabilities.items())
    draw = random.choices(choices, probs, k=1)[0]
    if draw == bet_number:
        return 2 * bet_amount
    else:
        return -bet_amount
