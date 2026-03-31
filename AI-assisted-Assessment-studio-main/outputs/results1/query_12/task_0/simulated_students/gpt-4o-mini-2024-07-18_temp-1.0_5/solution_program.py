def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            max_calories = 0
            max_dish = None
            for line in lines:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                dish, calories_str = line.split(',')
                try:
                    calories = int(calories_str)
                    if calories > max_calories:
                        max_calories = calories
                        max_dish = dish
                except ValueError:
                    return 'No valid data'
            if max_dish is None:
                return 'No valid data'
            return f'{max_dish}: {max_calories}'
    except FileNotFoundError:
        return 'No valid data'