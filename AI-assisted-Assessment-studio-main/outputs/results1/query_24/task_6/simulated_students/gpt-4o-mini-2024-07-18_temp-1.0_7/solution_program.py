def roll_dice(input_str):
    results = []
    rolls = input_str.split(',')
    for roll in rolls:
        try:
            num_dice, sides = roll.split('d')
            num_dice = int(num_dice)
            sides = int(sides)
            if num_dice < 1 or sides < 1:
                return 'Invalid number of dice or sides'
            total = num_dice * sides
            results.append(total)
        except (ValueError, IndexError):
            return 'Invalid roll format'
    return results