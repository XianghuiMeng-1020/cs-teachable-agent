def predict_winnings(numbers, bet_amounts):
    winning_number = 32
    total_payout = 0
    
    for number, bet in zip(numbers, bet_amounts):
        if number == winning_number:
            total_payout += bet * 36
    
    return total_payout