def check_dice_lottery_results(results):
    winning_results = []
    for die1, die2 in results:
        total = die1 + die2
        if total == 7 or total == 11:
            winning_results.append(True)
        elif die1 == die2 and total > 8:
            winning_results.append(True)
        else:
            winning_results.append(False)
    return winning_results