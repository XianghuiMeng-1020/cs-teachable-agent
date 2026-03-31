def manage_cookbook(cookbook, operation, recipe):
    name, ingredients = recipe

    if operation == 'add':
        if name not in cookbook:
            cookbook[name] = ingredients
    elif operation == 'update':
        if name in cookbook:
            cookbook[name] = ingredients
    elif operation == 'delete':
        if name in cookbook:
            del cookbook[name]

    return cookbook