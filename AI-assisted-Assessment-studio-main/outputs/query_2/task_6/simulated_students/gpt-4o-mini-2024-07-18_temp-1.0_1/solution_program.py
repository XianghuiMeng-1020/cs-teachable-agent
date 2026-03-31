def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as rf:
        recipes_content = rf.read().strip().split('\n\n')

    with open(available_file, 'r') as af:
        available_ingredients = set(line.strip().lower() for line in af)

    missing_ingredients = set()

    for recipe in recipes_content:
        lines = recipe.splitlines()
        if lines:
            for ingredient in lines[1:]:
                ingredient = ingredient.strip().lower()
                if ingredient and ingredient not in available_ingredients:
                    missing_ingredients.add(ingredient)

    with open(output_file, 'w') as of:
        for ingredient in sorted(missing_ingredients):
            of.write(ingredient + '\n')