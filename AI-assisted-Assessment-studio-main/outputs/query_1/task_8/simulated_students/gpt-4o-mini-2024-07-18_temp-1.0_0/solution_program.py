def pantheon_oracle(adventure_logs):
    fortune = 0
    count = {}  
    previous_creature = None
    streak_count = 0

    for creature in adventure_logs:
        if creature == previous_creature:
            streak_count += 1
        else:
            streak_count = 1

        if streak_count == 2:
            fortune -= 5
            count[previous_creature] = 0  
        elif streak_count == 3:
            fortune += 10
        elif streak_count == 7:
            fortune += 30

        previous_creature = creature
        count[creature] = streak_count

    return fortune