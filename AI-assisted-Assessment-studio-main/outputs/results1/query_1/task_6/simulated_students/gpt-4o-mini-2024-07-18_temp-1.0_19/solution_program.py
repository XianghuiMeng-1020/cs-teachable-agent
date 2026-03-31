def check_dice_lottery_results(results):
    outcomes = []
    for dice in results:
        sum_dice = sum(dice)
        if sum_dice == 7 or sum_dice == 11:
            outcomes.append(True)
        elif dice[0] == dice[1] and sum_dice > 8:
            outcomes.append(True)
        else:
            outcomes.append(False)
    return outcomes