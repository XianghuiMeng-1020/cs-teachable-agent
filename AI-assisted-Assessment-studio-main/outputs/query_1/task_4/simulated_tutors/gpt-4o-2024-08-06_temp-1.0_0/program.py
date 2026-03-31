def best_fruits(apples, min_value):
    # Filter the list to get all apples with a value greater than the min_value
    eligible_apples = [value for value in apples if value > min_value]
    
    # If fewer than two apples are eligible, return 0
    if len(eligible_apples) < 2:
        return 0
    
    # Sort the eligible values in descending order to find the top two
    eligible_apples.sort(reverse=True)
    
    # Return the sum of the top two age preservation values
    return eligible_apples[0] + eligible_apples[1]