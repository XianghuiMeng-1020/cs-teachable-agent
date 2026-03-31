def calculate_remaining_ingredients(recipe_path):
    # Read inventory from inventory.txt
    inventory = {}
    try:
        with open('inventory.txt', 'r') as inv_file:
            for line in inv_file:
                ingredient, quantity = line.strip().split()
                inventory[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError('Inventory file not found.')

    # Read recipe from the provided recipe_path
    recipe = {}
    try:
        with open(recipe_path, 'r') as rec_file:
            for line in rec_file:
                ingredient, quantity = line.strip().split()
                recipe[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError('Recipe file not found.')

    # Check if there are sufficient ingredients
    for ingredient, required in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < required:
            raise ValueError('Insufficient ingredients')

    # Calculate remaining ingredients
    remaining = {k: inventory[k] - recipe[k] for k in inventory}
    return remaining