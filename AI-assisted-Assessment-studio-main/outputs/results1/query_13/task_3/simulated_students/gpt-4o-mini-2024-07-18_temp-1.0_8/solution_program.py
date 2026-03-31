def calculate_remaining_ingredients(recipe_path):
    inventory = {}
    try:
        with open('inventory.txt', 'r') as inv_file:
            for line in inv_file:
                ingredient, quantity = line.strip().split()
                inventory[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError("The inventory file 'inventory.txt' was not found.")
    except ValueError:
        raise ValueError("The inventory file is incorrectly formatted.")

    recipe = {}
    try:
        with open(recipe_path, 'r') as rec_file:
            for line in rec_file:
                ingredient, quantity = line.strip().split()
                recipe[ingredient] = int(quantity)
    except FileNotFoundError:
        raise FileNotFoundError(f"The recipe file '{recipe_path}' was not found.")
    except ValueError:
        raise ValueError("The recipe file is incorrectly formatted.")

    for ingredient, req_quantity in recipe.items():
        if ingredient not in inventory or inventory[ingredient] < req_quantity:
            raise ValueError("Insufficient ingredients")

    remaining_ingredients = {ingredient: inventory[ingredient] - recipe.get(ingredient, 0) for ingredient in inventory}
    return remaining_ingredients