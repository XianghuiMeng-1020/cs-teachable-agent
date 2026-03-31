def calculate_winnings(bets, roll):
    net_winnings = 0
    for number in bets:
        bet_amount = bets[number]
        if number == roll:
            net_winnings += 3 * bet_amount
        else:
            net_winnings -= bet_amount
    return net_winnings