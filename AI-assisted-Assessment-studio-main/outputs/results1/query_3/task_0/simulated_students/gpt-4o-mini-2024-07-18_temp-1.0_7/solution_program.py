def calculate_winnings(bets, roll):
    net_winnings = 0
    for number in range(1, 7):
        amount = bets.get(number, 0)
        if number == roll:
            net_winnings += amount * 3
        else:
            net_winnings -= amount
    return net_winnings