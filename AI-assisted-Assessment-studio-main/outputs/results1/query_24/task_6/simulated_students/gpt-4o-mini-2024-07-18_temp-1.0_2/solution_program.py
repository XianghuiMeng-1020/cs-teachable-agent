def roll_dice(input_str):
    results = []
    rolls = input_str.split(',')
    for roll in rolls:
        if 'd' not in roll:
            return 'Invalid roll format'
        try:
            x, y = roll.split('d')
            x = int(x)
            y = int(y)
            if x < 1 or y < 1:
                return 'Invalid number of dice or sides'
        except ValueError:
            return 'Invalid roll format'
        results.append(x * y)
    return results