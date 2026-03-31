def dice_game(dice_rolls):
    results = []
    for roll in dice_rolls:
        sum_roll = sum(roll)
        if sum_roll in (7, 11):
            results.append("Win")
        elif sum_roll in (2, 3, 12):
            results.append("Lose")
        else:
            results.append("Neutral")
    return results