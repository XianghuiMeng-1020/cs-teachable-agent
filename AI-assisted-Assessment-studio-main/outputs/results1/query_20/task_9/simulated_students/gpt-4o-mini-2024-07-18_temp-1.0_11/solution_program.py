def calculate_score(controlled_territories, developed_territories):
    full_score = 8
    deduction = 3
    developed_points = full_score
    undeveloped_points = full_score - deduction

    score = 0
    for territory in controlled_territories:
        if territory in developed_territories:
            score += developed_points
        else:
            score += undeveloped_points

    return score