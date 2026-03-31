def dice_game(dice_rolls):
    outcomes = []
    for roll in dice_rolls:
        dice_sum = sum(roll)
        if dice_sum in (7, 11):
            outcomes.append("Win")
        elif dice_sum in (2, 3, 12):
            outcomes.append("Lose")
        else:
            outcomes.append("Neutral")
    return outcomes