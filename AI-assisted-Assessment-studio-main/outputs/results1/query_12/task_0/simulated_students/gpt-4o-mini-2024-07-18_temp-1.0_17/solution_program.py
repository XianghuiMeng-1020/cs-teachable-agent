def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return 'No valid data'

    if not lines:
        return 'No valid data'

    max_calories = -1
    dish_name = None

    for line in lines:
        line = line.strip()
        if ',' not in line or line.count(',') != 1:
            return 'No valid data'
        name, calorie_str = line.split(',', 1)
        try:
            calories = int(calorie_str)
        except ValueError:
            return 'No valid data'

        if calories > max_calories:
            max_calories = calories
            dish_name = name.strip()

    if dish_name is not None:
        return f'{dish_name}: {max_calories}'
    else:
        return 'No valid data'