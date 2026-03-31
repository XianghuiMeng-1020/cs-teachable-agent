def check_dice_lottery_results(results):
    winnings = []
    for die1, die2 in results:
        sum_dice = die1 + die2
        if sum_dice == 7 or sum_dice == 11:
            winnings.append(True)
        elif die1 == die2 and sum_dice > 8:
            winnings.append(True)
        else:
            winnings.append(False)
    return winnings