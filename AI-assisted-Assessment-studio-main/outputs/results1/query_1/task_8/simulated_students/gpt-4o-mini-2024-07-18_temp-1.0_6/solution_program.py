def predict_winnings(numbers, bet_amounts):
    total_payout = 0
    roulette_number = 32
    for number, bet in zip(numbers, bet_amounts):
        if number == roulette_number:
            total_payout += bet * 36
    return total_payout