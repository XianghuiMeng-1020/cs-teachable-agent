def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n\n')

    recipes = []
    for recipe in data:
        lines = recipe.strip().split('\n')
        if len(lines) > 0:
            recipe_name = lines[0]
            ingredients = lines[1:]  # all other lines are ingredients and quantities
            recipes.append((recipe_name, ingredients))

    recipes.sort(key=lambda x: x[0])

    with open(output_file, 'w') as f:
        for i, (name, ingredients) in enumerate(recipes):
            f.write(name + '\n')
            for ingredient in ingredients:
                f.write(ingredient + '\n')
            if i < len(recipes) - 1:
                f.write('\n')