def pantheon_oracle(adventure_logs):
    fortune = 0
    creature_count = 0
    current_creature = None

    for creature in adventure_logs:
        if creature == current_creature:
            creature_count += 1
            if creature_count == 3:
                fortune += 10  # Summon
            elif creature_count == 7:
                fortune += 30  # Divine Revelation
        else:
            if creature_count == 2:
                fortune -= 5  # False Echo
            current_creature = creature
            creature_count = 1  # Reset count to 1 for the new creature

    # final check for the last encountered creature
    if creature_count == 2:
        fortune -= 5  # Handle last creature's False Echo 
    elif creature_count == 3:
        fortune += 10  # Handle last creature's Summon
    elif creature_count == 7:
        fortune += 30  # Handle last creature's Divine Revelation

    return fortune