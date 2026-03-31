def roll_dice(input_str):
    result = []
    rolls = input_str.split(',')
    for roll in rolls:
        try:
            x, y = roll.lower().split('d')
            x = int(x)
            y = int(y)
            if x < 1 or y < 1:
                return 'Invalid number of dice or sides'
            result.append(x * y)
        except (ValueError, IndexError):
            return 'Invalid roll format'
    return result