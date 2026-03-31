def dice_game(num_rolls, dice_pairs):
    score = 0
    cumulative_scores = []
    for i in range(num_rolls):
        roll_sum = dice_pairs[i][0] + dice_pairs[i][1]
        if roll_sum == 7 or roll_sum == 11:
            score += 10
        elif roll_sum in {2, 3, 12}:
            score -= 5
        cumulative_scores.append(score)
    return cumulative_scores