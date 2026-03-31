def pantheon_oracle(adventure_logs):
    fortune = 0
    n = len(adventure_logs)
    count = 1
    current_creature = None

    for i in range(n):
        if adventure_logs[i] == current_creature:
            count += 1
        else:
            if count == 2:
                fortune -= 5  # False Echo if we had 2 in a row
            # Reset the count to 1 for the new creature
            current_creature = adventure_logs[i]  
            count = 1

        if count == 3:
            fortune += 10  # Summon
        elif count == 7:
            fortune += 30  # Divine Revelation

    # Final check if the last encounter was a False Echo
    if count == 2:
        fortune -= 5  # False Echo if we ended with 2 in a row

    return fortune