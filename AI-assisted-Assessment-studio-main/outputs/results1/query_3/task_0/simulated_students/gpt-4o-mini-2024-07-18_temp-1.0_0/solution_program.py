def calculate_winnings(bets, roll):
    total_winnings = 0
    for number, amount in bets.items():
        if number == roll:
            total_winnings += amount * 3
        else:
            total_winnings -= amount
    return total_winnings