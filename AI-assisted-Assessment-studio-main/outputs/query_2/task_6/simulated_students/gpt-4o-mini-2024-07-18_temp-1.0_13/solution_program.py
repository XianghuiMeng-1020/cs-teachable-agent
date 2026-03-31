def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as rfile:
        recipes = rfile.read()

    available_ingredients = set()
    with open(available_file, 'r') as afile:
        for line in afile:
            available_ingredients.add(line.strip().lower())

    missing_ingredients = set()
    recipes = recipes.strip().split('\n\n')
    for recipe in recipes:
        lines = recipe.strip().split('\n')
        for ingredient in lines[1:]:
            ingredient = ingredient.strip().lower()
            if ingredient and ingredient not in available_ingredients:
                missing_ingredients.add(ingredient)

    with open(output_file, 'w') as ofile:
        for ingredient in sorted(missing_ingredients):
            ofile.write(ingredient + '\n')