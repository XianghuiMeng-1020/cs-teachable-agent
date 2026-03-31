def predict_winnings(numbers, bet_amounts):
    outcome = 32
    total_payout = 0
    for number, bet in zip(numbers, bet_amounts):
        if number == outcome:
            total_payout += 36 * bet
    return total_payout