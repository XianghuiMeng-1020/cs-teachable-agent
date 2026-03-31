import random

def balance_predictor(bets, initial_balance, outcome_probabilities):
    balance = initial_balance
    for bet in bets:
        probability, multiplier = outcome_probabilities[bet]
        bet_amount = 100  # Assuming each bet is fixed at 100 for simplicity.
        roll = random.randint(1, 100)
        if roll < probability:
            balance += bet_amount * multiplier
        else:
            balance -= bet_amount
    return balance