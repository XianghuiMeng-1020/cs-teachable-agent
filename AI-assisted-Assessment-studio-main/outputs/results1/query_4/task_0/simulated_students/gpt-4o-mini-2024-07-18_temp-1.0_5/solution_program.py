def lucky_dice(outcomes):
    scores = []
    total_score = 0
    for roll in outcomes:
        current_sum = sum(roll)
        if current_sum in [7, 11]:
            scores.append(10)
            total_score += 10
        elif current_sum in [2, 3, 12]:
            scores.append(5)
            total_score += 5
        else:
            scores.append(0)
    return {'total_score': total_score, 'rolls': scores}