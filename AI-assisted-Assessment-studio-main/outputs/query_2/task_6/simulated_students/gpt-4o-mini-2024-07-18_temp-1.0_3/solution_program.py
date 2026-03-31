def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as rf:
        recipes_content = rf.read().strip()

    with open(available_file, 'r') as af:
        available_ingredients = set(line.strip().lower() for line in af if line.strip())

    missing_ingredients = set()
    recipes = recipes_content.split('\n\n')

    for recipe in recipes:
        lines = recipe.strip().splitlines()
        if lines:
            for ingredient in lines[1:]:
                ingredient = ingredient.strip().lower()
                if ingredient and ingredient not in available_ingredients:
                    missing_ingredients.add(ingredient)

    with open(output_file, 'w') as of:
        for ingredient in sorted(missing_ingredients):
            of.write(ingredient + '\n')