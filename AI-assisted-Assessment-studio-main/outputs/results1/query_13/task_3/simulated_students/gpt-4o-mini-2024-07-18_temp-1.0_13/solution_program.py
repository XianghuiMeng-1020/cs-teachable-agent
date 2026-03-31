def calculate_remaining_ingredients(recipe_path):
    try:
        with open('inventory.txt', 'r') as inventory_file:
            inventory = {}
            for line in inventory_file:
                ingredient, quantity = line.strip().split()
                inventory[ingredient] = int(quantity)

        with open(recipe_path, 'r') as recipe_file:
            recipe = {}
            for line in recipe_file:
                ingredient, quantity = line.strip().split()
                recipe[ingredient] = int(quantity)

        for ingredient, required_quantity in recipe.items():
            if ingredient not in inventory or inventory[ingredient] < required_quantity:
                raise ValueError('Insufficient ingredients')

        remaining = {key: inventory[key] - recipe.get(key, 0) for key in inventory}
        return remaining

    except FileNotFoundError:
        raise FileNotFoundError('One of the files was not found.')
    except Exception as e:
        raise e