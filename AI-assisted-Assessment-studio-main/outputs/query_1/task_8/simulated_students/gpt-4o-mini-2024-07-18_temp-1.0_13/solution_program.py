def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 1
    prev_creature = None

    for i in range(len(adventure_logs)):
        creature = adventure_logs[i]

        if creature == prev_creature:
            count += 1
        else:
            if count == 2:
                fortune -= 5  # False Echo
            elif count == 3:
                fortune += 10  # Summon
            elif count == 7:
                fortune += 30  # Divine Revelation
            count = 1  # reset count for new creature

        prev_creature = creature

    # Final check for the last sequence
    if count == 2:
        fortune -= 5  # False Echo
    elif count == 3:
        fortune += 10  # Summon
    elif count == 7:
        fortune += 30  # Divine Revelation

    return fortune