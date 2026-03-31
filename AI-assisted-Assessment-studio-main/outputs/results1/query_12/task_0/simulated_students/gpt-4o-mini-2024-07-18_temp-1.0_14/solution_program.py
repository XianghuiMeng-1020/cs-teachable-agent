def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 'No valid data'
            max_calories = -1
            dish_with_max_calories = ''
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) != 2:
                    return 'No valid data'
                dish = parts[0].strip()
                try:
                    calories = int(parts[1].strip())
                except ValueError:
                    return 'No valid data'
                if calories > max_calories:
                    max_calories = calories
                    dish_with_max_calories = dish
            return f'{dish_with_max_calories}: {max_calories}'
    except FileNotFoundError:
        return 'No valid data'