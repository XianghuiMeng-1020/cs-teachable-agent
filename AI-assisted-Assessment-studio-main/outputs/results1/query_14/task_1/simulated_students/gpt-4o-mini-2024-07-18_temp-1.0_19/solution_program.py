def manage_cookbook(cookbook, operation, recipe):
    if operation == 'add':
        recipe_name, ingredients = recipe
        if recipe_name not in cookbook:
            cookbook[recipe_name] = ingredients
    elif operation == 'update':
        recipe_name, ingredients = recipe
        if recipe_name in cookbook:
            cookbook[recipe_name] = ingredients
    elif operation == 'delete':
        recipe_name, _ = recipe
        if recipe_name in cookbook:
            del cookbook[recipe_name]
    return cookbook