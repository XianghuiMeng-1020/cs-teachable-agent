def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            max_calories = 0
            dish_name = ''
            for line in file:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                name, calories_str = line.split(',', 1)
                try:
                    calories = int(calories_str)
                except ValueError:
                    return 'No valid data'
                if calories > max_calories:
                    max_calories = calories
                    dish_name = name
            if dish_name:
                return f'{dish_name}: {max_calories}'
            else:
                return 'No valid data'
    except FileNotFoundError:
        return 'No valid data'
    except Exception:
        return 'No valid data'