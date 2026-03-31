def find_low_cal_recipes(threshold):
    low_cal_recipes = []
    try:
        with open('recipe_calories.txt', 'r') as file:
            for line in file:
                if line.strip():
                    name, calories = line.split(':')
                    calories = int(calories)
                    if calories <= threshold:
                        low_cal_recipes.append(name.strip())
    except FileNotFoundError:
        return []
    return low_cal_recipes