def dice_game(dice_rolls):
    results = []
    for roll in dice_rolls:
        total = sum(roll)
        if total == 7 or total == 11:
            results.append('Win')
        elif total in (2, 3, 12):
            results.append('Lose')
        else:
            results.append('Neutral')
    return results