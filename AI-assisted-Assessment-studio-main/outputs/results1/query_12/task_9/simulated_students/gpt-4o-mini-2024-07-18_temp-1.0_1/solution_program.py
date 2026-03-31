def find_low_cal_recipes(threshold):
    recipes_below_threshold = []
    try:
        with open('recipe_calories.txt', 'r') as file:
            for line in file:
                if line.strip():
                    recipe, calories = line.strip().split(': ')
                    if int(calories) <= threshold:
                        recipes_below_threshold.append(recipe)
    except FileNotFoundError:
        return []
    return recipes_below_threshold