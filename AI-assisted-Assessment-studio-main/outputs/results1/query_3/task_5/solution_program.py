def balance_predictor(bets, initial_balance, outcome_probabilities):
    from random import randint
    balance = initial_balance
    for bet in bets:
        prob, multiplier = outcome_probabilities[bet]
        if randint(1, 100) <= prob:
            balance += 10 * multiplier
        else:
            balance -= 10
    return balance
