def predict_winnings(numbers, bet_amounts):
    roulette_outcome = 32
    total_payout = 0
    for number, bet in zip(numbers, bet_amounts):
        if number == roulette_outcome:
            total_payout += 36 * bet
    return total_payout