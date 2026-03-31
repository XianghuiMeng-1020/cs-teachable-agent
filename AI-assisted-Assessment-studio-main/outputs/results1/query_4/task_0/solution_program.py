def lucky_dice(outcomes):
    scores = []
    total_score = 0
    score_mapping = {7: 10, 11: 10, 2: 5, 3: 5, 12: 5}
    for roll in outcomes:
        roll_sum = roll[0] + roll[1]
        score = score_mapping.get(roll_sum, 0)
        scores.append(score)
        total_score += score
    result = {
        "total_score": total_score,
        "rolls": scores
    }
    return result
