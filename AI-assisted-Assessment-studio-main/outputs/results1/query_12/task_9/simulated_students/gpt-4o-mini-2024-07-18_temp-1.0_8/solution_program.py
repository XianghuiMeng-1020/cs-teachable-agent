def find_low_cal_recipes(threshold):
    try:
        with open('recipe_calories.txt', 'r') as file:
            recipes = file.readlines()
            low_cal_recipes = []
            for recipe in recipes:
                name, cal = recipe.strip().split(': ')
                if int(cal) <= threshold:
                    low_cal_recipes.append(name)
            return low_cal_recipes
    except FileNotFoundError:
        return []
    except Exception:
        return []