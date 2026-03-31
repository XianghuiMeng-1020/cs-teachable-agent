def calculate_score(controlled_territories, developed_territories):
    full_points = 8
    deduction_points = 3
    score = 0
    developed_set = set(developed_territories)
    for territory in controlled_territories:
        if territory in developed_set:
            score += full_points
        else:
            score += (full_points - deduction_points)
    return score