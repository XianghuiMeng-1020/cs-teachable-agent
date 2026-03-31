def count_creature_types(creatures):
    creature_count = {}
    for creature in creatures:
        if creature in creature_count:
            creature_count[creature] += 1
        else:
            creature_count[creature] = 1
    return creature_count