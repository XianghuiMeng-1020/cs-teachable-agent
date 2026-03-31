def calculate_remaining_ingredients(recipe_path):
    try:
        with open('inventory.txt', 'r') as inv_file:
            inventory = {}
            for line in inv_file:
                parts = line.split()
                ingredient = parts[0]
                quantity = int(parts[1])
                inventory[ingredient] = quantity
    except IOError:
        raise IOError("Could not read inventory file")
    
    try:
        with open(recipe_path, 'r') as recipe_file:
            recipe = {}
            for line in recipe_file:
                parts = line.split()
                ingredient = parts[0]
                quantity = int(parts[1])
                recipe[ingredient] = quantity
    except IOError:
        raise IOError("Could not read recipe file")

    for ingredient, required_quantity in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < required_quantity:
            raise ValueError("Insufficient ingredients")

    remaining = {ingredient: inventory[ingredient] - recipe[ingredient] for ingredient in inventory}
    return remaining