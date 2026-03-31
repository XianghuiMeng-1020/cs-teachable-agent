def compute_total_calories(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return 'No valid data'
    
    max_calories = -1
    dish_name = ''
    for line in lines:
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
            dish_name = name.strip()
    
    if max_calories == -1:
        return 'No valid data'
    return f'{dish_name}: {max_calories}'