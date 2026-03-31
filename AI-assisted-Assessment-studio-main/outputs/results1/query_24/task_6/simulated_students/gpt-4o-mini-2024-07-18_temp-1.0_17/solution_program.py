def roll_dice(input_str):
    results = []
    rolls = input_str.split(',')
    for roll in rolls:
        try:
            # Split the roll into number of dice and sides
            num_dice, num_sides = roll.split('d')
            num_dice = int(num_dice)
            num_sides = int(num_sides)
            
            # Validate number of dice and sides
            if num_dice < 1 or num_sides < 1:
                return 'Invalid number of dice or sides'
            
            # Calculate total of simulated rolls (max possible value)
            total = num_dice * num_sides
            results.append(total)
        except ValueError:
            return 'Invalid roll format'
        except (IndexError, TypeError):
            return 'Invalid roll format'
    return results