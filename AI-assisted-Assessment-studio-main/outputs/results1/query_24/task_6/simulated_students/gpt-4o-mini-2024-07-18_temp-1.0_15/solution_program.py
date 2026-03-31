def roll_dice(input_str):
    results = []
    rolls = input_str.split(',')
    for roll in rolls:
        try:
            number, sides = roll.split('d')
            number = int(number)
            sides = int(sides)
            if number < 1 or sides < 1:
                return 'Invalid number of dice or sides'
            results.append(number * sides)
        except (ValueError, IndexError):
            return 'Invalid roll format'
    return results