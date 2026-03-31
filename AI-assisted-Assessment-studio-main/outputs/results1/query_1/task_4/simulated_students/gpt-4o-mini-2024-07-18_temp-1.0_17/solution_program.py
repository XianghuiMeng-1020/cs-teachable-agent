def dice_game(num_rolls, dice_pairs):
    cumulative_scores = []
    score = 0
    for i in range(num_rolls):
        d1, d2 = dice_pairs[i]
        total = d1 + d2
        if total in [7, 11]:
            score += 10
        elif total in [2, 3, 12]:
            score -= 5
        cumulative_scores.append(score)
    return cumulative_scores