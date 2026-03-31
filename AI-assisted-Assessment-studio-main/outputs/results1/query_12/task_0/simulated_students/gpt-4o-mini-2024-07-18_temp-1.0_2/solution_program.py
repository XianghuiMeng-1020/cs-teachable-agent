def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 'No valid data'
            max_calories = -1
            dish_name = None
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) != 2:
                    return 'No valid data'
                try:
                    name = parts[0].strip()
                    calories = int(parts[1].strip())
                    if calories > max_calories:
                        max_calories = calories
                        dish_name = name
                except ValueError:
                    return 'No valid data'
            if dish_name:
                return f'{dish_name}: {max_calories}'
            else:
                return 'No valid data'
    except FileNotFoundError:
        return 'No valid data'