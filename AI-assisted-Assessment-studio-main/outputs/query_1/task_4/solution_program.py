def best_fruits(apples, min_value):
    valid_apples = []
    for apple in apples:
        if apple > min_value:
            valid_apples.append(apple)
    if len(valid_apples) < 2:
        return 0
    valid_apples.sort(reverse=True)
    return valid_apples[0] + valid_apples[1]