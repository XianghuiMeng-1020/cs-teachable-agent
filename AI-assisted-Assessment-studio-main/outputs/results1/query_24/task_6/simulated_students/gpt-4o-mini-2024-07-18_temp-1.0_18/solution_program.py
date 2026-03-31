def roll_dice(input_str):
    results = []
    rolls = input_str.split(',')
    for roll in rolls:
        try:
            parts = roll.split('d')
            if len(parts) != 2:
                return 'Invalid roll format'
            num_dice = int(parts[0])
            num_sides = int(parts[1])
            if num_dice < 1 or num_sides < 1:
                return 'Invalid number of dice or sides'
            total = num_dice * num_sides
            results.append(total)
        except ValueError:
            return 'Invalid number of dice or sides'
    return results