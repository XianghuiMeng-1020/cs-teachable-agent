def roll_dice(input_str):
    rolls = input_str.split(',')
    results = []
    for roll in rolls:
        try:
            x, y = roll.split('d')
            x, y = int(x), int(y)
            if x < 1 or y < 1:
                return 'Invalid number of dice or sides'
            results.append(x * y)
        except (ValueError, IndexError):
            return 'Invalid roll format'
    return results