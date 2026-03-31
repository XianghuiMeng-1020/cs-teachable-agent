def calculate_winnings(bets, roll):
    total_winnings = 0
    for number, amount in bets.items():
        if number == roll:
            total_winnings += 3 * amount
        else:
            total_winnings -= amount
    return total_winnings