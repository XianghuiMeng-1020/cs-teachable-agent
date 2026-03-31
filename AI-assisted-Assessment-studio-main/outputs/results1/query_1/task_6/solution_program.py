def check_dice_lottery_results(results):
    win_results = []
    for roll in results:
        die1, die2 = roll
        dice_sum = die1 + die2
        if dice_sum == 7 or dice_sum == 11:
            win_results.append(True)
        elif die1 == die2 and dice_sum > 8:
            win_results.append(True)
        else:
            win_results.append(False)
    return win_results