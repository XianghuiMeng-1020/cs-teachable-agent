def calculate_remaining_ingredients(recipe_path):
    ingredients = {}
    # Read inventory from the file
    try:
        with open('inventory.txt', 'r') as inv_file:
            for line in inv_file:
                ingredient, quantity = line.split()
                ingredients[ingredient] = int(quantity)
    except IOError:
        raise IOError("Error reading inventory file")

    required_ingredients = {}
    # Read recipe from the provided path
    try:
        with open(recipe_path, 'r') as recipe_file:
            for line in recipe_file:
                ingredient, quantity = line.split()
                required_ingredients[ingredient] = int(quantity)
    except IOError:
        raise IOError("Error reading recipe file")

    for ingredient, required_quantity in required_ingredients.items():
        if ingredient not in ingredients or ingredients[ingredient] < required_quantity:
            raise ValueError("Insufficient ingredients")

    remaining_ingredients = {k: ingredients[k] - required_ingredients.get(k, 0) for k in ingredients}
    return remaining_ingredients