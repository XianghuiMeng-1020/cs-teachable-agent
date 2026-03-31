def calculate_score(controlled_territories, developed_territories):
    score = 0
    for territory in controlled_territories:
        if territory in developed_territories:
            score += 8
        else:
            score += 5
    return score