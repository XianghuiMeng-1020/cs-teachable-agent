def predict_winnings(numbers, bet_amounts):
    roulette_outcome = 32
    total_payout = 0
    for i in range(len(numbers)):
        if numbers[i] == roulette_outcome:
            total_payout += 36 * bet_amounts[i]
    return total_payout