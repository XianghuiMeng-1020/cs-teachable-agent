def check_dice_lottery_results(results):
    winning_results = []
    for dice in results:
        sum_dice = sum(dice)
        if sum_dice == 7 or sum_dice == 11:
            winning_results.append(True)
        elif dice[0] == dice[1] and sum_dice > 8:
            winning_results.append(True)
        else:
            winning_results.append(False)
    return winning_results