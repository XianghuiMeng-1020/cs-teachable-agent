def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            dishes = file.readlines()
            if not dishes:
                return 'No valid data'

            max_calories = -1
            max_dish = None

            for line in dishes:
                line = line.strip()
                if line.count(',') != 1:
                    return 'No valid data'
                dish, calories_str = line.split(',')
                try:
                    calories = int(calories_str)
                except ValueError:
                    return 'No valid data'

                if calories > max_calories:
                    max_calories = calories
                    max_dish = dish

            return f'{max_dish}: {max_calories}'
    except FileNotFoundError:
        return 'No valid data'