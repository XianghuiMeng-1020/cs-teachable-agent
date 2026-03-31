def roulette_game(money, bets):
    import random
    result = random.randint(1, 36)
    total_money = money
    if result % 2 == 0:  # result is even
        if "even" in bets:
            total_money += bets["even"]
    else:  # result is odd
        if "odd" in bets:
            total_money += bets["odd"]
    if "even" in bets:
        total_money -= bets["even"]
    if "odd" in bets:
        total_money -= bets["odd"]
    return total_money
