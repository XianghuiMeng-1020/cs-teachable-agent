def balance_predictor(bets, initial_balance, outcome_probabilities):
    import random
    balance = initial_balance
    for bet in bets:
        probability, multiplier = outcome_probabilities[bet]
        bet_amount = 100  # Assuming each bet is of fixed amount 100
        roll = random.randint(1, 100)  # Simulate a 100-sided die
        if roll < probability:
            balance += bet_amount * multiplier  # Win
        else:
            balance -= bet_amount  # Lose
    return balance