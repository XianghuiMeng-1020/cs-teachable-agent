import random

def balance_predictor(bets, initial_balance, outcome_probabilities):
    balance = initial_balance
    
    for bet in bets:
        bet_amount = 100  # Assuming a fixed bet amount of 100
        probability, multiplier = outcome_probabilities[bet]
        roll = random.randint(1, 100)

        if roll < probability:
            balance += bet_amount * multiplier
        else:
            balance -= bet_amount

    return balance