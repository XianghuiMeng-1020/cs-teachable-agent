def manage_cookbook(cookbook, operation, recipe):
    recipe_name, ingredients = recipe
    if operation == 'add':
        # Add the recipe only if it doesn't exist
        if recipe_name not in cookbook:
            cookbook[recipe_name] = ingredients
    elif operation == 'update':
        # Update the recipe if it exists
        if recipe_name in cookbook:
            cookbook[recipe_name] = ingredients
    elif operation == 'delete':
        # Delete the recipe if it exists
        if recipe_name in cookbook:
            del cookbook[recipe_name]
    return cookbook