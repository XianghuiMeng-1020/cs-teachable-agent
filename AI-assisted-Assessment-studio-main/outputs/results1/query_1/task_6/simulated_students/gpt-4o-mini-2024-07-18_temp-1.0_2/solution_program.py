def check_dice_lottery_results(results):
    winning_rolls = []
    for dice in results:
        sum_dice = sum(dice)
        if sum_dice == 7 or sum_dice == 11:
            winning_rolls.append(True)
        elif dice[0] == dice[1] and sum_dice > 8:
            winning_rolls.append(True)
        else:
            winning_rolls.append(False)
    return winning_rolls