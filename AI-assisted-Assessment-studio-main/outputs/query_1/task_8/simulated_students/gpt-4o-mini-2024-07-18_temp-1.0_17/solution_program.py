def pantheon_oracle(adventure_logs):
    fortune = 0
    current_creature = None
    count = 0
    previous_count = 0
    for creature in adventure_logs:
        if creature == current_creature:
            count += 1
        else:
            current_creature = creature
            count = 1

        if count == 2:
            previous_count = 0
            fortune -= 5
        elif count == 3:
            fortune += 10
            previous_count = 3
        elif count == 7:
            fortune += 30
            previous_count = 7
        else:
            if previous_count == 3:
                previous_count = 0
    return fortune