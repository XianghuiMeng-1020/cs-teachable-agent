def check_dice_lottery_results(results):
    outcomes = []
    for roll in results:
        dice1, dice2 = roll
        dice_sum = dice1 + dice2
        if dice_sum == 7 or dice_sum == 11:
            outcomes.append(True)
        elif dice1 == dice2 and dice_sum > 8:
            outcomes.append(True)
        else:
            outcomes.append(False)
    return outcomes