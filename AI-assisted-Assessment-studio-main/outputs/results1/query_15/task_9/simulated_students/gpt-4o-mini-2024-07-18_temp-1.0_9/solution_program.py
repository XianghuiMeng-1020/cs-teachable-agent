def count_creature_types(creatures):
    creature_counts = {}
    for creature in creatures:
        if creature in creature_counts:
            creature_counts[creature] += 1
        else:
            creature_counts[creature] = 1
    return creature_counts