def lucky_dice(outcomes):
    total_score = 0
    rolls = []
    for dice1, dice2 in outcomes:
        roll_sum = dice1 + dice2
        if roll_sum in (7, 11):
            score = 10
        elif roll_sum in (2, 3, 12):
            score = 5
        else:
            score = 0
        rolls.append(score)
        total_score += score
    return {'total_score': total_score, 'rolls': rolls}