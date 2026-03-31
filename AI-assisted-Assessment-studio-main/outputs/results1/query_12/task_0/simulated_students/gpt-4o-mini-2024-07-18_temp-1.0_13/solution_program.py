def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            max_calories = -1
            max_dish = None
            for line in lines:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                dish, calories = line.split(',', 1)
                try:
                    calories = int(calories)
                except ValueError:
                    return 'No valid data'
                if calories > max_calories:
                    max_calories = calories
                    max_dish = dish.strip()
            if max_dish is None:
                return 'No valid data'
            return f'{max_dish}: {max_calories}'
    except FileNotFoundError:
        return 'No valid data'