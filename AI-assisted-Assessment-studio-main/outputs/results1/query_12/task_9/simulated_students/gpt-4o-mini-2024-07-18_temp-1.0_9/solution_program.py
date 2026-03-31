def find_low_cal_recipes(threshold):
    recipes = []
    try:
        with open('recipe_calories.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    recipe, calories = line.split(': ')
                    if int(calories) <= threshold:
                        recipes.append(recipe)
    except FileNotFoundError:
        return []
    return recipes