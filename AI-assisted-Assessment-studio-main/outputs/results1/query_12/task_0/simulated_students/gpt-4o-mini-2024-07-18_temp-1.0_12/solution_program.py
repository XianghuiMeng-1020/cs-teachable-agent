def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 'No valid data'
            max_calories = -1
            dish_with_max_calories = None
            for line in lines:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                dish, calories_str = line.split(',', 1)
                try:
                    calories = int(calories_str)
                except ValueError:
                    return 'No valid data'
                if calories > max_calories:
                    max_calories = calories
                    dish_with_max_calories = dish
            if dish_with_max_calories:
                return f'{dish_with_max_calories}: {max_calories}'
            else:
                return 'No valid data'
    except FileNotFoundError:
        return 'No valid data'