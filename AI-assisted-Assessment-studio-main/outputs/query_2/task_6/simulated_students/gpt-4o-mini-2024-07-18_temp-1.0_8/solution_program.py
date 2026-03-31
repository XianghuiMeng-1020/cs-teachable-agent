def generate_shopping_list(recipes_file, available_file, output_file):
    with open(available_file, 'r') as f:
        available_ingredients = {line.strip().lower() for line in f.readlines()}

    missing_ingredients = set()
    with open(recipes_file, 'r') as f:
        recipes = f.read().strip().split('\n\n')
        for recipe in recipes:
            lines = recipe.splitlines()
            if len(lines) > 0:
                # Skip recipe name
                ingredients = lines[1:]
                for ingredient in ingredients:
                    ingredient = ingredient.strip().lower()
                    if ingredient and ingredient not in available_ingredients:
                        missing_ingredients.add(ingredient)

    with open(output_file, 'w') as f:
        for ingredient in sorted(missing_ingredients):
            f.write(ingredient + '\n')