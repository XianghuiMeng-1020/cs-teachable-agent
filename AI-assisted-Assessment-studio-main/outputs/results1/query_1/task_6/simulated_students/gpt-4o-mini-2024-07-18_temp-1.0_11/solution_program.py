def check_dice_lottery_results(results):
    winnings = []
    for die1, die2 in results:
        total = die1 + die2
        if total == 7 or total == 11:
            winnings.append(True)
        elif die1 == die2 and total > 8:
            winnings.append(True)
        else:
            winnings.append(False)
    return winnings