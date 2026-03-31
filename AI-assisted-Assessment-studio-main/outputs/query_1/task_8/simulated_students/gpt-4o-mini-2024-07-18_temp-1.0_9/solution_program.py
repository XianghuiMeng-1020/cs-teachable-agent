def pantheon_oracle(adventure_logs):
    fortune = 0
    current_creature = None
    current_count = 0
    count_map = {}
    previous_creature = None
    previous_count = 0

    for creature in adventure_logs:
        if creature == current_creature:
            current_count += 1
        else:
            if current_creature:
                count_map[current_creature] = current_count
            current_creature = creature
            current_count = 1

        if previous_creature == creature:
            if previous_count == 1:
                fortune -= 5  # False Echo
                current_count = 0  # Reset the count
            previous_count += 1
        else:
            previous_creature = creature
            previous_count = 1

        if current_count == 3:
            fortune += 10  # Summon
        elif current_count == 7:
            fortune += 30  # Divine Revelation

    if current_creature:
        count_map[current_creature] = current_count

    return fortune