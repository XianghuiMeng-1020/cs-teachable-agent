def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as rf:
        recipes_content = rf.read()

    recipes = recipes_content.strip().split('\n\n')
    available_ingredients = set()

    with open(available_file, 'r') as af:
        for line in af:
            available_ingredients.add(line.strip().lower())

    missing_ingredients = set()

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        ingredients = lines[1:]  # Skip the recipe name
        for ingredient in ingredients:
            ingredient = ingredient.strip().lower()
            if ingredient and ingredient not in available_ingredients:
                missing_ingredients.add(ingredient)

    with open(output_file, 'w') as of:
        for ingredient in sorted(missing_ingredients):
            of.write(ingredient + '\n')