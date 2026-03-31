def game_of_chance(bets, outcomes):
    balance = 100
    for bet, outcome in zip(bets, outcomes):
        if bet > balance:
            break
        if outcome in [4, 5, 6]:
            balance += bet  # Player wins, so add double the bet (bet + bet)
        else:
            balance -= bet  # Player loses, subtract the bet
    return balance