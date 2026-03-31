def calculate_mythical_power(affinities):
    total_power = 0
    for affinity in affinities:
        if affinity > 10:
            total_power += affinity * 2
        elif 5 <= affinity <= 10:
            total_power += affinity
        else:
            total_power -= affinity * 2
    return total_power