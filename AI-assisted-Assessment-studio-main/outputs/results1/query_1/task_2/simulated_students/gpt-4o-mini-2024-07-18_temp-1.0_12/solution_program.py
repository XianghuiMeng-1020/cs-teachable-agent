def spin_wheel(bet_list, target_number):
    total_winnings = 0
    for bet in bet_list:
        if bet[0] == target_number:
            total_winnings += bet[1] * 10
    return total_winnings