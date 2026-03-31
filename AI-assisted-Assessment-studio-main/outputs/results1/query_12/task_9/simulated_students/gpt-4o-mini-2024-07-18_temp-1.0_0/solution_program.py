def find_low_cal_recipes(threshold):
    low_cal_recipes = []
    try:
        with open('recipe_calories.txt', 'r') as file:
            for line in file:
                if line.strip():
                    recipe, calories = line.strip().split(':')
                    if int(calories) <= threshold:
                        low_cal_recipes.append(recipe.strip())
    except FileNotFoundError:
        return []
    return low_cal_recipes