def calculate_winnings(bets, roll):
    net_winning = 0
    for number, amount in bets.items():
        if number == roll:
            net_winning += amount * 3
        else:
            net_winning -= amount
    return net_winning