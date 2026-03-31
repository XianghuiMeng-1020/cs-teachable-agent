import random

def balance_predictor(bets, initial_balance, outcome_probabilities):
    balance = initial_balance
    
    for bet in bets:
        probability, multiplier = outcome_probabilities[bet]
        bet_amount = 100  # Fixed bet amount for simplicity
        roll = random.randint(1, 100)  # Simulating a 100-sided die
        
        if roll < probability:  # Player wins
            balance += bet_amount * multiplier
        else:  # Player loses
            balance -= bet_amount
    
    return balance