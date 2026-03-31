def calculate_mythical_power(affinities):
    total_power = 0
    for affinity in affinities:
        if affinity > 10:
            total_power += 2 * affinity
        elif 5 <= affinity <= 10:
            total_power += affinity
        elif affinity < 5:
            total_power -= 2 * affinity
    return total_power