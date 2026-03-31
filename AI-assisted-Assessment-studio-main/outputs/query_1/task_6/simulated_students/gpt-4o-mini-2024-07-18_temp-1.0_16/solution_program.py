def calculate_mythical_power(affinities):
    total_power = 0
    for value in affinities:
        if value > 10:
            total_power += 2 * value
        elif 5 <= value <= 10:
            total_power += value
        else:
            total_power -= 2 * value
    return total_power