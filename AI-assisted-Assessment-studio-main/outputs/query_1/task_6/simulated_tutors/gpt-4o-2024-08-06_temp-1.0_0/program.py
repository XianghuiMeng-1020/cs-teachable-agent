def calculate_mythical_power(affinities):
    # Initialize total power to 0
    total_power = 0
    
    # Iterate over each affinity to calculate its contribution to the mythical power
    for affinity in affinities:
        if affinity > 10:  # Strong affinities
            total_power += 2 * affinity
        elif 5 <= affinity <= 10:  # Moderate affinities
            total_power += affinity
        elif affinity < 5:  # Weak affinities
            total_power -= 2 * affinity
    
    # Return the total calculated mythical power
    return total_power