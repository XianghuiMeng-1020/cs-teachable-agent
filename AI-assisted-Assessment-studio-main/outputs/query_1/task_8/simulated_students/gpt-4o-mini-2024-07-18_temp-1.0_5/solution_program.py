def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 0
    last_creature = None
    last_count = 0
    creature_counts = {}

    for creature in adventure_logs:
        if creature == last_creature:
            count += 1
        else:
            count = 1
            last_creature = creature

        if count == 3:
            fortune += 10
            last_count = 3  # Mark as a summon
        elif count == 7:
            fortune += 30
            last_count = 7  # Mark as a divine revelation
        elif count == 2:
            fortune -= 5
            last_count = 2  # Mark as a false echo

        if creature not in creature_counts:
            creature_counts[creature] = 0
        creature_counts[creature] += 1

        # Reset the counts if necessary
        if last_count == 2 and creature_counts[creature] > 2:
            creature_counts[creature] = 1

    return fortune