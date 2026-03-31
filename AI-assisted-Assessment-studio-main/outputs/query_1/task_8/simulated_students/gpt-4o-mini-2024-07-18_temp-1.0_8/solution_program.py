def pantheon_oracle(adventure_logs):
    fortune = 0
    current_creature = None
    current_count = 0

    for creature in adventure_logs:
        if creature == current_creature:
            current_count += 1
        else:
            current_creature = creature
            current_count = 1

        if current_count == 2:
            fortune -= 5
            current_count = 0  # Reset count for False Echo
        elif current_count == 3:
            fortune += 10
        elif current_count == 7:
            fortune += 30

    return fortune