def find_low_cal_recipes(threshold):
    try:
        with open('recipe_calories.txt', 'r') as file:
            lines = file.readlines()
        recipes = []
        for line in lines:
            if line.strip():
                name, calories = line.split(':')
                calories = int(calories.strip())
                if calories <= threshold:
                    recipes.append(name.strip())
        return recipes
    except FileNotFoundError:
        return []
    except Exception:
        return []