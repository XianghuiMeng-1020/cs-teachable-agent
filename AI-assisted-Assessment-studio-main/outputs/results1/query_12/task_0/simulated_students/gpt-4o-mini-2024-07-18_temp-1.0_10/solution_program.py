def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 'No valid data'
            max_calories = -1
            dish_name = ''
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) != 2:
                    return 'No valid data'
                name, calories_str = parts[0].strip(), parts[1].strip()
                try:
                    calories = int(calories_str)
                    if calories > max_calories:
                        max_calories = calories
                        dish_name = name
                except ValueError:
                    return 'No valid data'
            if max_calories == -1:
                return 'No valid data'
            return f'{dish_name}: {max_calories}'
    except FileNotFoundError:
        return 'No valid data'