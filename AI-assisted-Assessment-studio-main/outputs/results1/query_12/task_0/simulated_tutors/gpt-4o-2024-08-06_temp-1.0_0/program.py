def compute_total_calories(filename):
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            max_calories = -1
            max_dish = ''
            # Read each line in the file
            for line in file:
                # Strip any leading/trailing whitespace
                line = line.strip()
                # Split the line by comma
                parts = line.split(',')
                # Check for two parts (dish name and calories)
                if len(parts) == 2:
                    try:
                        # Extract dish name and calories
                        dish_name = parts[0].strip()
                        calories = int(parts[1].strip())
                        # Update max dish and calories if current is higher
                        if calories > max_calories:
                            max_calories = calories
                            max_dish = dish_name
                    except ValueError:
                        # If calories is not an integer, skip this line
                        continue
                else:
                    # If the line is not in the expected format, skip it
                    continue
            # Check if max_calories has been updated
            if max_calories != -1:
                return f'{max_dish}: {max_calories}'
            else:
                return 'No valid data'
    except FileNotFoundError:
        return 'No valid data'