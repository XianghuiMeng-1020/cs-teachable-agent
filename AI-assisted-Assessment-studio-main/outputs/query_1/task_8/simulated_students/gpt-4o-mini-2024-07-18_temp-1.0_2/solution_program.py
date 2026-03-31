def pantheon_oracle(adventure_logs):
    fortune = 0
    count = {}  # to keep track of counts for each creature
    prev_creature = None  # to track the previous creature in the meantime
    streak = 0  # to track consecutive encounters

    for creature in adventure_logs:
        if creature == prev_creature:
            streak += 1
            # Check for Divine Revelation
            if streak == 7:
                fortune += 30
                # Reset streak to zero after Divine Revelation
                streak = 0
            # Check for Summon
            elif streak == 3:
                fortune += 10
        else:
            # If there's a different creature, we check for False Echo
            if streak == 2:
                fortune -= 5  # apply False Echo

            # Reset the counters
            count[creature] = count.get(creature, 0) + 1
            streak = 1  # reset streak to 1 for the new creature

        prev_creature = creature  # update the previous creature

    # Final check for False Echo when the loop ends
    if streak == 2:
        fortune -= 5

    return fortune