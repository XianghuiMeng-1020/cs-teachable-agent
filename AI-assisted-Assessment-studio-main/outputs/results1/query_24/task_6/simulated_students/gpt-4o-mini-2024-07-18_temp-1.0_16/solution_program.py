def roll_dice(input_str):
    results = []
    rolls = input_str.split(',')
    for roll in rolls:
        try:
            dice_info = roll.split('d')
            if len(dice_info) != 2:
                return 'Invalid roll format'
            X = int(dice_info[0])
            y = int(dice_info[1])
            if X < 1 or y < 1:
                return 'Invalid number of dice or sides'
            results.append(X * y)
        except ValueError:
            return 'Invalid number of dice or sides'
    return results