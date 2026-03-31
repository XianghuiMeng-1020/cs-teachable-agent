def check_dice_lottery_results(results):
    outcomes = []
    for die1, die2 in results:
        total = die1 + die2
        if total == 7 or total == 11:
            outcomes.append(True)
        elif die1 == die2 and total > 8:
            outcomes.append(True)
        else:
            outcomes.append(False)
    return outcomes