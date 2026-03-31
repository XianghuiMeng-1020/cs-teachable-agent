import random


def simulate_game(bet_number, bet_amount, probabilities):
    outcome = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    if outcome == bet_number:
        return 2 * bet_amount
    else:
        return -bet_amount