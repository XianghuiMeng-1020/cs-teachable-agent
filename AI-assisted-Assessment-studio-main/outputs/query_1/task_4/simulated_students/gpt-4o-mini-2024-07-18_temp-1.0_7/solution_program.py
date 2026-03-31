def best_fruits(apples, min_value):
    filtered_apples = [value for value in apples if value > min_value]
    if len(filtered_apples) < 2:
        return 0
    top_two = sorted(filtered_apples, reverse=True)[:2]
    return sum(top_two)