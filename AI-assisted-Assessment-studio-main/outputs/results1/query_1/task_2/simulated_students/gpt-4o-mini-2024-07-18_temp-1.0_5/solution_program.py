def spin_wheel(bet_list, target_number):
    total_winnings = 0
    for number, bet_amount in bet_list:
        if number == target_number:
            total_winnings += bet_amount * 10
    return total_winnings