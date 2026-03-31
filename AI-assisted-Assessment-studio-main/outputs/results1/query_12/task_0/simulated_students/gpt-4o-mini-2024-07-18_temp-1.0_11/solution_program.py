def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            max_calories = 0
            max_dish = None
            for line in file:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                dish, calories_str = line.split(',', 1)
                try:
                    calories = int(calories_str)
                    if calories > max_calories:
                        max_calories = calories
                        max_dish = dish.strip()
                except ValueError:
                    return 'No valid data'
            if max_dish:
                return f'{max_dish}: {max_calories}'
            else:
                return 'No valid data'
    except FileNotFoundError:
        return 'No valid data'