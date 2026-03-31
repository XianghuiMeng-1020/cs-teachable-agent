def predict_winnings(numbers, bet_amounts):
    total_payout = 0
    outcome = 32
    for number, bet in zip(numbers, bet_amounts):
        if number == outcome:
            total_payout += bet * 36
    return total_payout