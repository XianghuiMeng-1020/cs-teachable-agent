def predict_winnings(numbers, bet_amounts):
    payout = 0
    for i in range(len(numbers)):
        if numbers[i] == 32:
            payout += 36 * bet_amounts[i]
    return payout