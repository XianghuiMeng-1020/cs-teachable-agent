def spin_wheel(bet_list, target_number):
    total_won = 0
    for number, amount in bet_list:
        if number == target_number:
            total_won += amount * 10
    return total_won