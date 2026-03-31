def check_dice_lottery_results(results):
    winnings = []
    for roll in results:
        a, b = roll
        total = a + b
        if total == 7 or total == 11:
            winnings.append(True)
        elif a == b and total > 8:
            winnings.append(True)
        else:
            winnings.append(False)
    return winnings