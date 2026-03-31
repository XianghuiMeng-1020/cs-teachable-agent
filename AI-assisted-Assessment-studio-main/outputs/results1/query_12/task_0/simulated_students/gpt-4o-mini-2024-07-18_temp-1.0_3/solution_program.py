def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            max_calories = -1
            max_dish = None
            for line in file:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                dish, calories = line.split(',')
                dish = dish.strip()
                calories = calories.strip()
                if not calories.isdigit() or not dish:
                    return 'No valid data'
                calories = int(calories)
                if calories > max_calories:
                    max_calories = calories
                    max_dish = dish
            if max_dish is None:
                return 'No valid data'
            return f'{max_dish}: {max_calories}'
    except FileNotFoundError:
        return 'No valid data'