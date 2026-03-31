import random

def balance_predictor(bets, initial_balance, outcome_probabilities):
    balance = initial_balance
    for bet in bets:
        if bet in outcome_probabilities:
            probability, multiplier = outcome_probabilities[bet]
            if random.randint(1, 100) < probability:
                balance += 10 * multiplier
            else:
                balance -= 10
    return balance