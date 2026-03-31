def predict_winnings(numbers, bet_amounts):
    winning_number = 32
    total_payout = 0
    for i in range(len(numbers)):
        if numbers[i] == winning_number:
            total_payout += 36 * bet_amounts[i]
    return total_payout