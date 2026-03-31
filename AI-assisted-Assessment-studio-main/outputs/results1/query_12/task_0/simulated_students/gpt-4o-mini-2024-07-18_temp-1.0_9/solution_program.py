def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        if not lines:
            return 'No valid data'
        max_calories = 0
        dish_name = ''
        for line in lines:
            line = line.strip()
            if line.count(',') != 1:
                return 'No valid data'
            name, calories = line.split(',')
            try:
                calories = int(calories)
            except ValueError:
                return 'No valid data'
            if calories > max_calories:
                max_calories = calories
                dish_name = name.strip()
        return f'{dish_name}: {max_calories}'
    except FileNotFoundError:
        return 'No valid data'