def roll_dice(input_str):
    results = []
    rolls = input_str.split(',')
    for roll in rolls:
        try:
            # Split the string into X and y components
            x_str, y_str = roll.split('d')
            # Convert X and y to integers
            X = int(x_str)
            y = int(y_str)
            # Validate X and y
            if X < 1 or y < 1:
                return 'Invalid number of dice or sides'
            # Calculate sum of the maximum possible roll
            total = X * y
            results.append(total)
        except (ValueError, IndexError):
            return 'Invalid roll format'
    return results