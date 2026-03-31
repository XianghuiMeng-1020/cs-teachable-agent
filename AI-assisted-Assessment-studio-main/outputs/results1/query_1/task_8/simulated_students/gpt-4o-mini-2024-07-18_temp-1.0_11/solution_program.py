def predict_winnings(numbers, bet_amounts):
    payout = 0
    winning_number = 32
    for num, bet in zip(numbers, bet_amounts):
        if num == winning_number:
            payout += 36 * bet
    return payout