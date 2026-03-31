def spin_wheel(bet_list, target_number):
    total_won = 0
    for bet in bet_list:
        number, amount = bet
        if number == target_number:
            total_won += amount * 10
    return total_won