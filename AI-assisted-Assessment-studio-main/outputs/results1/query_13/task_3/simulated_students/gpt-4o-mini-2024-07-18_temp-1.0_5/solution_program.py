def calculate_remaining_ingredients(recipe_path):
    try:
        with open('inventory.txt', 'r') as inv_file:
            inventory = {}
            for line in inv_file:
                ingredient, quantity = line.strip().split()
                inventory[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError("Inventory file not found")
    except Exception as e:
        raise Exception(f"An error occurred while reading the inventory: {e}")

    try:
        with open(recipe_path, 'r') as rec_file:
            recipe = {}
            for line in rec_file:
                ingredient, quantity = line.strip().split()
                recipe[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError("Recipe file not found")
    except Exception as e:
        raise Exception(f"An error occurred while reading the recipe: {e}")

    for ingredient, required_amount in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < required_amount:
            raise ValueError("Insufficient ingredients")

    remaining_inventory = inventory.copy()
    for ingredient, required_amount in recipe.items():
        remaining_inventory[ingredient] -= required_amount

    return remaining_inventory