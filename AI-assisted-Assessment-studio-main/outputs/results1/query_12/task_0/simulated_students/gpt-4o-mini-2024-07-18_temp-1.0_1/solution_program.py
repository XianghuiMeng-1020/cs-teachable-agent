def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            highest_calorie_dish = None
            highest_calories = 0
            for line in file:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                dish, calories_str = line.split(',')
                try:
                    calories = int(calories_str)
                except ValueError:
                    return 'No valid data'
                if calories > highest_calories:
                    highest_calories = calories
                    highest_calorie_dish = dish.strip()
            if highest_calorie_dish:
                return f'{highest_calorie_dish}: {highest_calories}'
            else:
                return 'No valid data'
    except FileNotFoundError:
        return 'No valid data'