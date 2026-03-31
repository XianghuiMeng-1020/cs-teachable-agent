def roll_dice(input_str):
    rolls = input_str.split(',')
    results = []
    for roll in rolls:
        try:
            num_dice, num_sides = roll.split('d')
            num_dice = int(num_dice)
            num_sides = int(num_sides)
            if num_dice < 1 or num_sides < 1:
                return 'Invalid number of dice or sides'
            results.append(num_dice * num_sides)
        except ValueError:
            return 'Invalid roll format'
        except Exception:
            return 'Invalid number of dice or sides'
    return results