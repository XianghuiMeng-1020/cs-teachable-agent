def pantheon_oracle(adventure_logs):
    fortune = 0
    current_count = 0
    previous_creature = None
    false_echo = False
    index = 0
    length = len(adventure_logs)

    while index < length:
        creature = adventure_logs[index]
        if creature == previous_creature:
            current_count += 1
        else:
            if current_count == 2:
                false_echo = True
            elif current_count == 3:
                fortune += 10
            elif current_count == 7:
                fortune += 30

            current_count = 1  # reset count for the new creature
            previous_creature = creature
            false_echo = False  # reset false echo flag
        index += 1

    # Final check for the last sequence
    if current_count == 2:
        false_echo = True
    elif current_count == 3:
        fortune += 10
    elif current_count == 7:
        fortune += 30

    if false_echo:
        fortune -= 5

    return fortune