import random

def balance_predictor(bets, initial_balance, outcome_probabilities):
    balance = initial_balance
    
    for bet in bets:
        probability, multiplier = outcome_probabilities[bet]
        bet_amount = 100  # Assuming each bet is a fixed amount of 100
        roll = random.randint(1, 100)  # Simulate a roll of a 100-sided die
        
        if roll < probability:
            balance += bet_amount * multiplier
        else:
            balance -= bet_amount
    
    return balance