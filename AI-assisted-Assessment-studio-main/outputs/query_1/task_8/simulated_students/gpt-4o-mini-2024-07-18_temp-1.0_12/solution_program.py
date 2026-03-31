def pantheon_oracle(adventure_logs):
    fortune = 0
    current_count = 1
    current_creature = None

    for i in range(len(adventure_logs)):
        if i > 0:
            if adventure_logs[i] == current_creature:
                current_count += 1
            else:
                current_creature = adventure_logs[i]
                current_count = 1

        # Check for False Echo
        if current_count == 2:
            fortune -= 5
            current_count = 0  # Reset count after False Echo; emulate effect
            continue

        # Check for Summon
        if current_count == 3:
            fortune += 10

        # Check for Divine Revelation
        if current_count == 7:
            fortune += 30

    return fortune