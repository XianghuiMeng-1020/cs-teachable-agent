def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as r_file:
        recipes_data = r_file.read()

    with open(available_file, 'r') as a_file:
        available_ingredients = {line.strip().lower() for line in a_file}

    recipes = recipes_data.strip().split('\n\n')
    missing_ingredients = set()

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        for ingredient in lines[1:]:
            ingredient = ingredient.strip().lower()
            if ingredient and ingredient not in available_ingredients:
                missing_ingredients.add(ingredient)

    with open(output_file, 'w') as o_file:
        for item in sorted(missing_ingredients):
            o_file.write(item + '\n')