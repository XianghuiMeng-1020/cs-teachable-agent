def find_low_cal_recipes(threshold):
    recipes = []
    try:
        with open('recipe_calories.txt', 'r') as file:
            for line in file:
                if line.strip():
                    name, calories = line.strip().split(': ')
                    if int(calories) <= threshold:
                        recipes.append(name)
    except FileNotFoundError:
        return []
    except ValueError:
        return []
    return recipes