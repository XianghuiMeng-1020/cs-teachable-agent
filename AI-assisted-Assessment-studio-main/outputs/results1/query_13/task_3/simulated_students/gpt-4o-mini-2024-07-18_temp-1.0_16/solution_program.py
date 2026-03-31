def calculate_remaining_ingredients(recipe_path):
    inventory = {}
    try:
        with open('inventory.txt', 'r') as f:
            for line in f:
                ingredient, quantity = line.split()
                inventory[ingredient] = int(quantity)
    except Exception as e:
        raise RuntimeError('Error reading inventory file') from e

    recipe = {}
    try:
        with open(recipe_path, 'r') as f:
            for line in f:
                ingredient, quantity = line.split()
                recipe[ingredient] = int(quantity)
    except Exception as e:
        raise RuntimeError('Error reading recipe file') from e

    for ingredient, req_quantity in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < req_quantity:
            raise ValueError('Insufficient ingredients')

    remaining = {ingredient: inventory[ingredient] - recipe.get(ingredient, 0) for ingredient in inventory}

    return remaining