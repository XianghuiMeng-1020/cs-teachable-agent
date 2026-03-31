def roll_dice(input_str):
    rolls = input_str.split(',')
    results = []
    for roll in rolls:
        try:
            x_d_y = roll.lower().strip().split('d')
            if len(x_d_y) != 2:
                return 'Invalid roll format'
            x = int(x_d_y[0])
            y = int(x_d_y[1])
            if x < 1 or y < 1:
                return 'Invalid number of dice or sides'
            results.append(x * y)
        except ValueError:
            return 'Invalid number of dice or sides'
    return results