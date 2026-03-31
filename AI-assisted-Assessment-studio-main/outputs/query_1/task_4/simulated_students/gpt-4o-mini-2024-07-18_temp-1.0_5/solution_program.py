def best_fruits(apples, min_value):
    filtered_apples = [value for value in apples if value > min_value]
    if len(filtered_apples) < 2:
        return 0
    filtered_apples.sort(reverse=True)
    return filtered_apples[0] + filtered_apples[1]