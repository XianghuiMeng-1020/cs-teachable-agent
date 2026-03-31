def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as recipes:
        recipe_contents = recipes.read().strip().split('\n\n')

    with open(available_file, 'r') as available:
        available_ingredients = set(line.strip().lower() for line in available if line.strip())

    missing_ingredients = set()

    for recipe in recipe_contents:
        lines = recipe.strip().split('\n')
        for ingredient in lines[1:]:
            ingredient = ingredient.strip().lower()
            if ingredient and ingredient not in available_ingredients:
                missing_ingredients.add(ingredient)

    with open(output_file, 'w') as output:
        for ingredient in sorted(missing_ingredients):
            output.write(f'{ingredient}\n')