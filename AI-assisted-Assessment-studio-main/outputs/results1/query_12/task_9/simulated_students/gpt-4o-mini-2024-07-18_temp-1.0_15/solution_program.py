def find_low_cal_recipes(threshold):
    try:
        with open('recipe_calories.txt', 'r') as file:
            low_cal_recipes = []
            for line in file:
                if line.strip():
                    recipe, calories = line.split(':')
                    calories = int(calories.strip())
                    if calories <= threshold:
                        low_cal_recipes.append(recipe.strip())
            return low_cal_recipes
    except FileNotFoundError:
        return []
    except Exception:
        return []