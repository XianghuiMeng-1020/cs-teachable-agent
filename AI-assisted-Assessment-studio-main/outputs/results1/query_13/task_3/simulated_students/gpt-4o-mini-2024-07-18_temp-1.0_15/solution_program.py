def calculate_remaining_ingredients(recipe_path):
    try:
        with open('inventory.txt', 'r') as inv_file:
            inventory = {}
            for line in inv_file:
                ingredient, quantity = line.strip().split()
                inventory[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError("The inventory file does not exist.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the inventory: {e}")

    try:
        with open(recipe_path, 'r') as recipe_file:
            recipe = {}
            for line in recipe_file:
                ingredient, quantity = line.strip().split()
                recipe[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError("The recipe file does not exist.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the recipe: {e}")

    for ingredient, required_quantity in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < required_quantity:
            raise ValueError("Insufficient ingredients")

    remaining_ingredients = inventory.copy()
    for ingredient, required_quantity in recipe.items():
        remaining_ingredients[ingredient] -= required_quantity

    return remaining_ingredients