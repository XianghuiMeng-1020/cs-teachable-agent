def calculate_winnings(bets, roll):
    net_winnings = 0
    for number in range(1, 7):
        if number in bets:
            if number == roll:
                net_winnings += bets[number] * 3
            else:
                net_winnings -= bets[number]
    return net_winnings