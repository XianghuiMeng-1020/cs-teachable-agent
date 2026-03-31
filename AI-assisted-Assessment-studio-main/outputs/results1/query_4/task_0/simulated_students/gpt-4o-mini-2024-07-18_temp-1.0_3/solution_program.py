def lucky_dice(outcomes):
    total_score = 0
    rolls = []
    for roll in outcomes:
        die1, die2 = roll
        total = die1 + die2
        if total in [7, 11]:
            score = 10
        elif total in [2, 3, 12]:
            score = 5
        else:
            score = 0
        rolls.append(score)
        total_score += score
    return {'total_score': total_score, 'rolls': rolls}