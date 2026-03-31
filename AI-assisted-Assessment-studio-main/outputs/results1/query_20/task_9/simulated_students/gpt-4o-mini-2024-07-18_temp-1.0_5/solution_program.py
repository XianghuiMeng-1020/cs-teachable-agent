def calculate_score(controlled_territories, developed_territories):
    score = 0
    developed_set = set(developed_territories)
    for territory in controlled_territories:
        if territory in developed_set:
            score += 8
        else:
            score += 5
    return score