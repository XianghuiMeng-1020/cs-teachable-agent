def calculate_winnings(bets, roll):
    total_winnings = 0
    for number, bet in bets.items():
        if number == roll:
            total_winnings += bet * 3
        else:
            total_winnings -= bet
    return total_winnings