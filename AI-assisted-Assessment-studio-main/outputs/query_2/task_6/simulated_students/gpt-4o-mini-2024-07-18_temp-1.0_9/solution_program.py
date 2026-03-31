def generate_shopping_list(recipes_file, available_file, output_file):
    with open(available_file, 'r') as av_file:
        available_ingredients = set(line.strip().lower() for line in av_file)

    missing_ingredients = set()

    with open(recipes_file, 'r') as rec_file:
        recipes = rec_file.read().strip().split('\n\n')
        for recipe in recipes:
            lines = recipe.strip().split('\n')
            if len(lines) > 0:
                recipe_name = lines[0].strip()  # Recipe name
                ingredients = [line.strip().lower() for line in lines[1:]]
                for ingredient in ingredients:
                    if ingredient not in available_ingredients:
                        missing_ingredients.add(ingredient)

    with open(output_file, 'w') as out_file:
        for ingredient in sorted(missing_ingredients):
            out_file.write(ingredient + '\n')