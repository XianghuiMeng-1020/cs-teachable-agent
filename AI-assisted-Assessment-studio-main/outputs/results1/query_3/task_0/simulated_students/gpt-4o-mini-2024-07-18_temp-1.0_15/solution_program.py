def calculate_winnings(bets, roll):
    winnings = 0
    for number, bet in bets.items():
        if number == roll:
            winnings += bet * 3
        else:
            winnings -= bet
    return winnings