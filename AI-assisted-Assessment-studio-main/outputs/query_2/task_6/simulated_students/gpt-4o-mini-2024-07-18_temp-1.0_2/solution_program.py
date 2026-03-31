def generate_shopping_list(recipes_file, available_file, output_file):
    with open(available_file, 'r') as f:
        available_ingredients = {line.strip().lower() for line in f if line.strip()}

    missing_ingredients = set()

    with open(recipes_file, 'r') as f:
        recipes = f.read().strip().split('\n\n')  # Split recipes by empty line
        for recipe in recipes:
            lines = recipe.strip().split('\n')
            ingredients = lines[1:]  # Skip the first line (recipe name)
            for ingredient in ingredients:
                if ingredient.strip().lower() not in available_ingredients:
                    missing_ingredients.add(ingredient.strip())

    with open(output_file, 'w') as f:
        for ingredient in sorted(missing_ingredients):
            f.write(ingredient + '\n')