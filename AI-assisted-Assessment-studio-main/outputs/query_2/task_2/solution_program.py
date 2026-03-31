def get_recipes_by_category(filename, category_name):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    recipes = []
    for line in lines:
        parts = line.strip().split(';')
        if len(parts) != 4:
            continue

        name, ingredients, prep_time, category = parts
        if category.lower() == category_name.lower():
            recipes.append(name)

    return recipes