def calculate_remaining_ingredients(recipe_path):
    try:
        with open('inventory.txt', 'r') as inventory_file:
            inventory = {}
            for line in inventory_file:
                ingredient, quantity = line.split()
                inventory[ingredient] = int(quantity)

        with open(recipe_path, 'r') as recipe_file:
            recipe = {}
            for line in recipe_file:
                ingredient, quantity = line.split()
                recipe[ingredient] = int(quantity)

        for ingredient, required_quantity in recipe.items():
            if ingredient not in inventory or inventory[ingredient] < required_quantity:
                raise ValueError('Insufficient ingredients')
            inventory[ingredient] -= required_quantity

        return {ingredient: quantity for ingredient, quantity in inventory.items() if quantity > 0}

    except FileNotFoundError:
        raise FileNotFoundError('One of the files could not be found')
    except ValueError as ve:
        raise ve
    except Exception:
        raise Exception('An error occurred while processing the files')