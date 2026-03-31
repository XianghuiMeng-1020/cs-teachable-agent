def calculate_remaining_ingredients(recipe_path):
    inventory = {}
    try:
        with open('inventory.txt', 'r') as inv_file:
            for line in inv_file:
                ingredient, quantity = line.split()
                inventory[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError("Inventory file not found.")
    except Exception as e:
        raise Exception(f"Error reading inventory: {e}")

    recipe = {}
    try:
        with open(recipe_path, 'r') as recipe_file:
            for line in recipe_file:
                ingredient, quantity = line.split()
                recipe[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError("Recipe file not found.")
    except Exception as e:
        raise Exception(f"Error reading recipe: {e}")

    for ingredient, required_quantity in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < required_quantity:
            raise ValueError("Insufficient ingredients")

    remaining_ingredients = {ingredient: inventory[ingredient] - recipe[ingredient] for ingredient in inventory}
    return remaining_ingredients