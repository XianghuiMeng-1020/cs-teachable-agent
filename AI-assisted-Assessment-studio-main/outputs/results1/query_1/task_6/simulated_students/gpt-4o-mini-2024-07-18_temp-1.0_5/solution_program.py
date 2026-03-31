def check_dice_lottery_results(results):
    winning_results = []
    for result in results:
        die1, die2 = result
        sum_dice = die1 + die2
        if sum_dice == 7 or sum_dice == 11:
            winning_results.append(True)
        elif die1 == die2 and sum_dice > 8:
            winning_results.append(True)
        else:
            winning_results.append(False)
    return winning_results