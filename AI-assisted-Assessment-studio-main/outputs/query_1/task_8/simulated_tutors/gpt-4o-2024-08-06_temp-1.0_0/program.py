def pantheon_oracle(adventure_logs):
    current_creature = None
    current_count = 0
    fortune = 0

    for creature in adventure_logs:
        if creature == current_creature:
            current_count += 1
            if current_count == 2:
                fortune -= 5  # False Echo
            elif current_count == 3:
                fortune += 10  # Summon
            elif current_count == 7:
                fortune += 30  # Divine Revelation
                current_count = 0  # Reset the count after revelation
        else:
            current_creature = creature
            current_count = 1

    return fortune