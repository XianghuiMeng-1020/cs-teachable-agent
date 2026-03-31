def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as f:
        recipes_content = f.read()

    recipes = [recipe.strip().split('\n') for recipe in recipes_content.split('\n\n')]
    all_ingredients = set()
    
    for recipe in recipes:
        recipe_name = recipe[0]  # First line is the recipe name
        ingredients = recipe[1:]  # Remaining lines are the ingredients
        all_ingredients.update(map(str.lower, ingredients))

    with open(available_file, 'r') as f:
        available_ingredients = set(map(str.lower, f.read().strip().split('\n')))

    missing_ingredients = sorted(all_ingredients - available_ingredients)

    with open(output_file, 'w') as f:
        for ingredient in missing_ingredients:
            f.write(ingredient + '\n')