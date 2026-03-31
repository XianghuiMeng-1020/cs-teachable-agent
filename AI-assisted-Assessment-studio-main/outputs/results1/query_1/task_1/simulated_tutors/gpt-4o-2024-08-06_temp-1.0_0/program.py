def dice_game(dice_rolls):
    outcomes = []
    for roll in dice_rolls:
        sum_of_dice = sum(roll)
        if sum_of_dice in [7, 11]:
            outcomes.append("Win")
        elif sum_of_dice in [2, 3, 12]:
            outcomes.append("Lose")
        else:
            outcomes.append("Neutral")
    return outcomes