def count_creature_types(creatures):
    counts = {}
    for creature in creatures:
        if creature in counts:
            counts[creature] += 1
        else:
            counts[creature] = 1
    return counts