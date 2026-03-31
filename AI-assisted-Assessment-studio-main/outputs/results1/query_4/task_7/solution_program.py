def dice_probability(target_score):
    outcomes = 36
    score_combinations = {}
    for a in range(1, 7):
        for b in range(1, 7):
            score = a + b
            if score not in score_combinations:
                score_combinations[score] = 0
            score_combinations[score] += 1
    if target_score < 2 or target_score > 12:
        return 0
    favorable_outcomes = score_combinations.get(target_score, 0)
    probability = favorable_outcomes / outcomes
    return round(probability, 4)