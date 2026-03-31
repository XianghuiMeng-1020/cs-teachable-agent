def calculate_remaining_ingredients(recipe_path):
    # Read inventory from inventory.txt
    try:
        with open('inventory.txt', 'r') as inv_file:
            inventory = {}
            for line in inv_file:
                ingredient, quantity = line.strip().split()
                inventory[ingredient] = int(quantity)
    except Exception as e:
        raise ValueError(f"Error reading inventory: {str(e)}")

    # Read recipe from the provided recipe path
    try:
        with open(recipe_path, 'r') as recipe_file:
            recipe = {}
            for line in recipe_file:
                ingredient, quantity = line.strip().split()
                recipe[ingredient] = int(quantity)
    except Exception as e:
        raise ValueError(f"Error reading recipe: {str(e)}")

    # Check if recipe can be prepared
    for ingredient, required_quantity in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < required_quantity:
            raise ValueError("Insufficient ingredients")

    # Calculate remaining ingredients
    remaining_ingredients = {ingredient: inventory[ingredient] - recipe.get(ingredient, 0) for ingredient in inventory}

    return remaining_ingredients