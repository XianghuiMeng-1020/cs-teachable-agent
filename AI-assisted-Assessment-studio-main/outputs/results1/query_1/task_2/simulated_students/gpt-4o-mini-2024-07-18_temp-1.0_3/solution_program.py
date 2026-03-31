def spin_wheel(bet_list, target_number):
    total_won = 0
    for bet in bet_list:
        bet_number, bet_amount = bet
        if bet_number == target_number:
            total_won += bet_amount * 10
    return total_won