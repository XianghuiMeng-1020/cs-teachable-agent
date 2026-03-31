def pantheon_oracle(adventure_logs):
    fortune = 0
    current_creature = None
    current_count = 0
    previous_count = 0
    false_echo_active = False

    for creature in adventure_logs:
        if creature == current_creature:
            current_count += 1
            if current_count == 2:
                false_echo_active = True
                current_count = 0  # Reset count after false echo
            elif current_count == 3:
                fortune += 10  # Summon
            elif current_count == 7:
                fortune += 30  # Divine Revelation
        else:
            if false_echo_active:
                false_echo_active = False  # Reset false echo flag
            else:
                previous_count = current_count
            current_creature = creature
            current_count = 1  # Reset count for new creature

    return fortune