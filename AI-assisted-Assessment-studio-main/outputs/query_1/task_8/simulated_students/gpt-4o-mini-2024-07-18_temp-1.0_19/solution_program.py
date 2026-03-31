def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 1
    previous_creature = None

    for i in range(len(adventure_logs)):
        if adventure_logs[i] == previous_creature:
            count += 1
        else:
            if count == 2:
                fortune -= 5  # False Echo
            count = 1

        if count == 3:
            fortune += 10  # Summon
        elif count == 7:
            fortune += 30  # Divine Revelation

        previous_creature = adventure_logs[i]

    if count == 2:
        fortune -= 5  # Handle the last counts
    return fortune