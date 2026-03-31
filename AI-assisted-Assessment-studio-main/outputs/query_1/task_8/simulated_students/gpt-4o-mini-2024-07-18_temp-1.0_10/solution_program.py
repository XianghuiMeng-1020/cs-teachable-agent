def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 0
    previous_creature = None
    previous_count = 0

    for creature in adventure_logs:
        if creature == previous_creature:
            count += 1
        else:
            if count == 2:
                fortune -= 5  # False Echo
            if count == 3:
                fortune += 10  # Summon
            if count == 7:
                fortune += 30  # Divine Revelation
            previous_creature = creature
            previous_count = count
            count = 1

    # Check the last sequence
    if count == 2:
        fortune -= 5  # False Echo
    if count == 3:
        fortune += 10  # Summon
    if count == 7:
        fortune += 30  # Divine Revelation

    return fortune