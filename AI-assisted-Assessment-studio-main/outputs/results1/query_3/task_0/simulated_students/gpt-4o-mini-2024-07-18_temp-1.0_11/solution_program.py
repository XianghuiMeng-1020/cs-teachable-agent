def calculate_winnings(bets, roll):
    net_winnings = 0
    for number, amount in bets.items():
        if number == roll:
            net_winnings += amount * 3
        else:
            net_winnings -= amount
    return net_winnings