def predict_winnings(numbers, bet_amounts):
    winning_number = 32
    total_payout = 0
    for number, bet_amount in zip(numbers, bet_amounts):
        if number == winning_number:
            total_payout += 36 * bet_amount
    return total_payout