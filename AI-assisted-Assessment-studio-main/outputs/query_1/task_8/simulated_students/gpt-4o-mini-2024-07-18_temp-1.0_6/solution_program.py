def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 0
    current_creature = None
    previous_creature = None
    last_count = 0

    for creature in adventure_logs:
        if creature == current_creature:
            count += 1
            # If we reached 3 counts, it's a summon
            if count == 3:
                fortune += 10
            # If we reached 7 counts, it's a divine revelation
            elif count == 7:
                fortune += 30
        else:
            # If we've encountered a different creature, check the previous count
            if count == 2:
                fortune -= 5  # false echo upon encountering 2
            current_creature = creature
            previous_creature = current_creature
            count = 1  # reset count for the new creature

    # After the loop, we need to check the last recorded counts for false echo
    if count == 2:
        fortune -= 5

    return fortune