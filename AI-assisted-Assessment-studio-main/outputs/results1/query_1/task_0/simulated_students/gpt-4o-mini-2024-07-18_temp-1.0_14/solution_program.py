def game_of_chance(bets, outcomes):
    balance = 100
    for bet, outcome in zip(bets, outcomes):
        if bet > balance:
            break
        if outcome >= 4:
            balance += bet  # Player wins and gets double the bet amount
        else:
            balance -= bet  # Player loses the bet amount
    return balance