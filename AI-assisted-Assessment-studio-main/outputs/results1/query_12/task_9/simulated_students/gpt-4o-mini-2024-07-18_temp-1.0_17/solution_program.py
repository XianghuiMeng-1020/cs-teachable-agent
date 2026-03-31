def find_low_cal_recipes(threshold):
    low_cal_recipes = []
    try:
        with open('recipe_calories.txt', 'r') as file:
            for line in file:
                if line.strip():  
                    recipe, calories = line.split(':')
                    recipe = recipe.strip()
                    calories = int(calories.strip())
                    if calories <= threshold:
                        low_cal_recipes.append(recipe)
    except FileNotFoundError:
        pass
    return low_cal_recipes