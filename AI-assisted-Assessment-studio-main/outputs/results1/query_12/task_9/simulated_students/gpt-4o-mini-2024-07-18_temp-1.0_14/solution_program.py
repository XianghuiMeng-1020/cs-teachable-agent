def find_low_cal_recipes(threshold):
    try:
        with open('recipe_calories.txt', 'r') as file:
            recipes = file.readlines()
    except FileNotFoundError:
        return []
    
    low_cal_recipes = []
    
    for recipe in recipes:
        if recipe.strip():
            name, calories = recipe.split(':')
            calories = int(calories.strip())
            if calories <= threshold:
                low_cal_recipes.append(name.strip())
    
    return low_cal_recipes