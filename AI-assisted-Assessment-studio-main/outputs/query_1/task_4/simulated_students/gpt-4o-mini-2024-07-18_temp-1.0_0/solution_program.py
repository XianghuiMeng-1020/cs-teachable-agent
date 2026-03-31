def best_fruits(apples, min_value):
    # Filter apples to only include those greater than min_value
    valid_apples = [apple for apple in apples if apple > min_value]
    # Sort the valid apples in descending order
    valid_apples.sort(reverse=True)
    # Check if we have at least two apples
    if len(valid_apples) < 2:
        return 0
    # Return the sum of the top two apples
    return valid_apples[0] + valid_apples[1]