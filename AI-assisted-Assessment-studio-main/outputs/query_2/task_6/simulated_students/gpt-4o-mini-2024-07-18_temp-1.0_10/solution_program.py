def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as r_file:
        recipes_content = r_file.read()

    with open(available_file, 'r') as a_file:
        available_ingredients = {line.strip().lower() for line in a_file}

    missing_ingredients = set()

    recipes = recipes_content.strip().split('\n\n')
    for recipe in recipes:
        lines = recipe.strip().split('\n')
        ingredients = [line.strip().lower() for line in lines[1:]]
        for ingredient in ingredients:
            if ingredient not in available_ingredients:
                missing_ingredients.add(ingredient)

    with open(output_file, 'w') as o_file:
        for ingredient in sorted(missing_ingredients):
            o_file.write(ingredient + '\n')