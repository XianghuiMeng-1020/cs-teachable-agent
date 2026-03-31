def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as recipes:
        recipes_content = recipes.read()
    recipes_list = [recipe.strip().split('\n')[1:] for recipe in recipes_content.strip().split('\n\n')]
    available_ingredients = set()
    with open(available_file, 'r') as available:
        available_ingredients = {line.strip().lower() for line in available}
    missing_ingredients = set()
    for recipe in recipes_list:
        for ingredient in recipe:
            if ingredient.strip().lower() not in available_ingredients:
                missing_ingredients.add(ingredient.strip())
    with open(output_file, 'w') as output:
        for ingredient in sorted(missing_ingredients):
            output.write(ingredient + '\n')