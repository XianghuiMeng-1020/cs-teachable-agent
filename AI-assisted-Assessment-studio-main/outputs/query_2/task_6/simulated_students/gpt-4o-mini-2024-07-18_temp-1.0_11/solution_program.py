def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as r_file:
        recipes = r_file.read().strip().split('\n\n')

    with open(available_file, 'r') as a_file:
        available = {line.strip().lower() for line in a_file.readlines()}

    missing_ingredients = set()

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        ingredients = lines[1:]
        for ingredient in ingredients:
            if ingredient.strip().lower() not in available:
                missing_ingredients.add(ingredient.strip())

    with open(output_file, 'w') as o_file:
        for ingredient in sorted(missing_ingredients):
            o_file.write(ingredient + '\n')