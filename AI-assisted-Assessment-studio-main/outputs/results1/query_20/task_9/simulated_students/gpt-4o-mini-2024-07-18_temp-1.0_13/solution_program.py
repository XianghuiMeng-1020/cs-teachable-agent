def calculate_score(controlled_territories, developed_territories):
    total_score = 0
    developed_set = set(developed_territories)
    for territory in controlled_territories:
        if territory in developed_set:
            total_score += 8
        else:
            total_score += 5
    return total_score