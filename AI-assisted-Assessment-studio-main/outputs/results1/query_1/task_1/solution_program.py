def dice_game(dice_rolls):
    outcomes = []
    for roll in dice_rolls:
        total = roll[0] + roll[1]
        if total in [7, 11]:
            outcomes.append('Win')
        elif total in [2, 3, 12]:
            outcomes.append('Lose')
        else:
            outcomes.append('Neutral')
    return outcomes
