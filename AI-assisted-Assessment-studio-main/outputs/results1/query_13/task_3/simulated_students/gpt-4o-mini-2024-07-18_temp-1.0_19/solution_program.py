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

        for ingredient, required in recipe.items():
            if ingredient not in inventory or inventory[ingredient] < required:
                raise ValueError('Insufficient ingredients')

        remaining = {ingredient: inventory[ingredient] - recipe.get(ingredient, 0) for ingredient in inventory}
        return remaining

    except FileNotFoundError:
        raise FileNotFoundError('The specified file was not found.')
    except Exception as e:
        raise Exception(f'An error occurred: {e}')