import random


def simulate_game(bet_number, bet_amount, probabilities):
    drawn_number = random.choices(range(1, 11), weights=probabilities.values())[0]
    if drawn_number == bet_number:
        return bet_amount * 2
    else:
        return -bet_amount