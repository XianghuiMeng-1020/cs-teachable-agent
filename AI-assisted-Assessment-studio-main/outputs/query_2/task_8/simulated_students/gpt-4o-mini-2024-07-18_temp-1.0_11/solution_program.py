def filter_ingredients(input_file, output_file, max_ingredients):
    recipes = []
    with open(input_file, 'r') as file:
        recipe = []
        for line in file:
            line = line.strip()
            if line:
                recipe.append(line)
            elif recipe:
                recipes.append(recipe)
                recipe = []
        if recipe:
            recipes.append(recipe)  # Add the last recipe if any

    filtered_recipes = []
    for recipe in recipes:
        if len(recipe) > 1 and len(recipe) - 1 <= max_ingredients:
            filtered_recipes.append(recipe)

    with open(output_file, 'w') as file:
        for recipe in filtered_recipes:
            file.write(f'{recipe[0]}\n')
            for ingredient in recipe[1:]:
                file.write(f'{ingredient}\n')
            file.write('\n')