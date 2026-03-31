import random

def balance_predictor(bets, initial_balance, outcome_probabilities):
    balance = initial_balance
    
    for bet in bets:
        if bet in outcome_probabilities:
            probability, multiplier = outcome_probabilities[bet]
            stake = 100  # Fixed bet amount per bet
            if random.randint(1, 100) < probability:
                balance += stake * multiplier
            else:
                balance -= stake
    
    return balance