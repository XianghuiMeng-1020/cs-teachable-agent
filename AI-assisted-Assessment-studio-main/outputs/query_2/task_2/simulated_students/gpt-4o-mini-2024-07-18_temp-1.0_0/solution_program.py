def get_recipes_by_category(filename, category_name):
    recipes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) != 4:
                    continue  # skip invalid lines
                recipe_name, ingredients, prep_time, category = parts
                if category.strip().lower() == category_name.strip().lower():
                    recipes.append(recipe_name.strip())
    except FileNotFoundError:
        return []
    except Exception:
        return []

    return recipes
