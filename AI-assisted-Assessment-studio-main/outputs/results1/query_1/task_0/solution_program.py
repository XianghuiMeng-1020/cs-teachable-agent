def game_of_chance(bets, outcomes):
    balance = 100
    for bet, outcome in zip(bets, outcomes):
        if balance <= 0:
            break
        if bet > balance:
            continue
        if outcome in [4, 5, 6]:
            balance += bet
        else:
            balance -= bet
    return balance