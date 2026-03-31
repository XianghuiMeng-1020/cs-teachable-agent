def roll_dice(input_str):
    try:
        rolls = input_str.split(',')
        sums = []
        for roll in rolls:
            if 'd' not in roll:
                return 'Invalid roll format'
            dice, sides = roll.split('d')
            try:
                dice = int(dice)
                sides = int(sides)
                if dice < 1 or sides < 1:
                    return 'Invalid number of dice or sides'
                sums.append(dice * sides)
            except ValueError:
                return 'Invalid number of dice or sides'
        return sums
    except:
        return 'Invalid roll format'