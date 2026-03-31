def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 0
    prev_creature = None
    prev_count = 0

    for creature in adventure_logs:
        if creature == prev_creature:
            count += 1
        else:
            count = 1
            prev_creature = creature

        if count == 2:
            fortune -= 5  # False Echo
            prev_count = 0  # reset count for this creature
        elif count == 3:
            fortune += 10  # Summon
            prev_count += 3  # keep track of previous sum
        elif count == 7:
            fortune += 30  # Divine Revelation
            prev_count += 7  # keep track of previous sum
            count = 0  # reset count after Divine Revelation

    return fortune