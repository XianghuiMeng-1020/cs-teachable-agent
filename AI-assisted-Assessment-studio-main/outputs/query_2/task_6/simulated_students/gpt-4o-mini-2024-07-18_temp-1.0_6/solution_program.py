def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as recipes:
        recipe_lines = recipes.read().strip().split('\n\n')

    with open(available_file, 'r') as available:
        available_ingredients = {line.strip().lower() for line in available}

    missing_ingredients = set()

    for recipe in recipe_lines:
        lines = recipe.strip().split('\n')
        for line in lines[1:]:  # Skip the first line which is the recipe name
            ingredient = line.strip().lower()
            if ingredient and ingredient not in available_ingredients:
                missing_ingredients.add(ingredient)

    with open(output_file, 'w') as output:
        for ingredient in sorted(missing_ingredients):
            output.write(ingredient + '\n')