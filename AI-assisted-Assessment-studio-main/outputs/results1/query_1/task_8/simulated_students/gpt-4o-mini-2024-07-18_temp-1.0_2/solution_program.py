def predict_winnings(numbers, bet_amounts):
    payout = 0
    result_number = 32
    for number, bet in zip(numbers, bet_amounts):
        if number == result_number:
            payout += bet * 36
    return payout