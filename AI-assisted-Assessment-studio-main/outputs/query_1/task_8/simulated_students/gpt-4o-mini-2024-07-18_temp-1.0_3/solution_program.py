def pantheon_oracle(adventure_logs):
    fortune = 0
    current_creature = None
    current_count = 0
    previous_creature = None
    previous_count = 0

    for creature in adventure_logs:
        if creature == current_creature:
            current_count += 1
        else:
            if current_count == 3:
                fortune += 10
            elif current_count == 7:
                fortune += 30
            # Check for False Echo
            if current_count == 2 and previous_creature == current_creature:
                fortune -= 5

            previous_creature = current_creature
            previous_count = current_count
            current_creature = creature
            current_count = 1

    # Final check at the end of the list
    if current_count == 3:
        fortune += 10
    elif current_count == 7:
        fortune += 30
    if current_count == 2 and previous_creature == current_creature:
        fortune -= 5

    return fortune