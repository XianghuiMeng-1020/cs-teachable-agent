def predict_winnings(numbers, bet_amounts):
    total_payout = 0
    winning_number = 32
    
    for i in range(len(numbers)):
        if numbers[i] == winning_number:
            total_payout += bet_amounts[i] * 36
    
    return total_payout