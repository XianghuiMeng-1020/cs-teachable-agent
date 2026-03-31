def manage_cookbook(cookbook, operation, recipe):
    recipe_name, ingredients = recipe

    if operation == 'add':
        if recipe_name not in cookbook:
            cookbook[recipe_name] = ingredients
    elif operation == 'update':
        if recipe_name in cookbook:
            cookbook[recipe_name] = ingredients
    elif operation == 'delete':
        if recipe_name in cookbook:
            del cookbook[recipe_name]

    return cookbook