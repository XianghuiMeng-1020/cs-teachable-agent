def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as rf:
        recipes_content = rf.read()

    with open(available_file, 'r') as af:
        available_ingredients = set(line.strip().lower() for line in af)

    recipes = recipes_content.strip().split('\n\n')
    missing_ingredients = set()

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        if len(lines) > 0:
            for ingredient in lines[1:]:
                ingredient_clean = ingredient.strip().lower()
                if ingredient_clean not in available_ingredients:
                    missing_ingredients.add(ingredient.strip())

    with open(output_file, 'w') as of:
        for ingredient in sorted(missing_ingredients):
            of.write(ingredient + '\n')