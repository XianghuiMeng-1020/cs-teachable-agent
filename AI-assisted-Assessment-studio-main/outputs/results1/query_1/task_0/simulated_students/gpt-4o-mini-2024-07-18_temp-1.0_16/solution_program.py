def game_of_chance(bets, outcomes):
    balance = 100
    for bet, outcome in zip(bets, outcomes):
        if bet > balance:
            break
        if outcome in [4, 5, 6]:
            balance += bet
        elif outcome in [1, 2, 3]:
            balance -= bet
    return balance