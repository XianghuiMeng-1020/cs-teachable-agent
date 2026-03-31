def pantheon_oracle(adventure_logs):
    fortune = 0
    count = 1
    previous_creature = None
    last_count = 0

    for i in range(len(adventure_logs)):
        current_creature = adventure_logs[i]

        if current_creature == previous_creature:
            count += 1
        else:
            if count == 2:
                fortune -= 5  # False Echo
            elif count == 3:
                fortune += 10  # Summon
            elif count >= 7:
                fortune += 30  # Divine Revelation

            previous_creature = current_creature
            count = 1

        if i == len(adventure_logs) - 1:
            # Check the last encountered creature after the loop
            if count == 2:
                fortune -= 5  # False Echo
            elif count == 3:
                fortune += 10  # Summon
            elif count >= 7:
                fortune += 30  # Divine Revelation

    return fortune