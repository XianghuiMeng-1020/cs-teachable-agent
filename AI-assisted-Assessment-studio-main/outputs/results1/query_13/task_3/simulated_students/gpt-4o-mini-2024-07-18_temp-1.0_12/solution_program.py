def calculate_remaining_ingredients(recipe_path):
    inventory = {}
    try:
        with open('inventory.txt', 'r') as inv_file:
            for line in inv_file:
                ingredient, quantity = line.strip().split()  
                inventory[ingredient] = int(quantity)
    except IOError:
        raise IOError("Error reading inventory file.")

    recipe = {}
    try:
        with open(recipe_path, 'r') as rec_file:
            for line in rec_file:
                ingredient, quantity = line.strip().split()
                recipe[ingredient] = int(quantity)
    except IOError:
        raise IOError("Error reading recipe file.")

    for ingredient, required in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < required:
            raise ValueError("Insufficient ingredients")

    remaining = {ingredient: inventory[ingredient] - recipe.get(ingredient, 0) for ingredient in inventory}
    return remaining