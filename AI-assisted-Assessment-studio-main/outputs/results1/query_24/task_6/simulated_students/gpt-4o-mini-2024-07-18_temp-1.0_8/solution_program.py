def roll_dice(input_str):
    rolls = input_str.split(',')
    results = []
    for roll in rolls:
        try:
            parts = roll.split('d')
            if len(parts) != 2:
                return 'Invalid roll format'
            x = int(parts[0])
            y = int(parts[1])
            if x < 1 or y < 1:
                return 'Invalid number of dice or sides'
            roll_sum = x * y
            results.append(roll_sum)
        except ValueError:
            return 'Invalid number of dice or sides'
    return results