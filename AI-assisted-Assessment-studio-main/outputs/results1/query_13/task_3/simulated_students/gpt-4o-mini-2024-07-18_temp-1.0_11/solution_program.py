def calculate_remaining_ingredients(recipe_path):
    try:
        with open('inventory.txt', 'r') as inv_file:
            inventory = {}
            for line in inv_file:
                ingredient, quantity = line.split()  
                inventory[ingredient] = int(quantity)

        with open(recipe_path, 'r') as rec_file:
            recipe = {}
            for line in rec_file:
                ingredient, quantity = line.split()  
                recipe[ingredient] = int(quantity)

        for ingredient, quantity in recipe.items():
            if ingredient not in inventory or inventory[ingredient] < quantity:
                raise ValueError('Insufficient ingredients')

        remaining_ingredients = {ingredient: inventory[ingredient] - recipe[ingredient] for ingredient in inventory}
        return remaining_ingredients
    except FileNotFoundError:
        raise FileNotFoundError('One or more files not found')
    except Exception as e:
        raise Exception(f'Something went wrong: {e}')