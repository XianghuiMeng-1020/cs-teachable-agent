def dice_game(dice_rolls):
    outcomes = []
    for roll in dice_rolls:
        total = sum(roll)
        if total in {7, 11}:
            outcomes.append('Win')
        elif total in {2, 3, 12}:
            outcomes.append('Lose')
        else:
            outcomes.append('Neutral')
    return outcomes