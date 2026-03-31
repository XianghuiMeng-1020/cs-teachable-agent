def generate_shopping_list(recipes_file, available_file, output_file):
    with open(available_file, 'r') as af:
        available = {line.strip().lower() for line in af if line.strip()}

    missing_ingredients = set()

    with open(recipes_file, 'r') as rf:
        recipes = rf.read().strip().split('\n\n')
        for recipe in recipes:
            lines = recipe.strip().splitlines()  
            if len(lines) > 1:
                recipe_name = lines[0].strip()  
                ingredients = {line.strip().lower() for line in lines[1:] if line.strip()}
                missing_ingredients.update(ingredients - available)

    with open(output_file, 'w') as of:
        for ingredient in sorted(missing_ingredients):
            of.write(ingredient + '\n')