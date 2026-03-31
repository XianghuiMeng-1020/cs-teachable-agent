def find_low_cal_recipes(threshold):
    try:
        with open('recipe_calories.txt', 'r') as file:
            recipes = file.readlines()
    except FileNotFoundError:
        return []
    if not recipes:
        return []
    low_cal_recipes = []
    for recipe in recipes:
        name, calories = recipe.strip().split(': ')
        if int(calories) <= threshold:
            low_cal_recipes.append(name)
    return low_cal_recipes