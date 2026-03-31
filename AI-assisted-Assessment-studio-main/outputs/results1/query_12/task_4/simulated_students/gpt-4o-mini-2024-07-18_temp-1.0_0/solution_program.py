def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read().strip().split('\n\n')

    recipes = []

    for recipe in content:
        lines = recipe.strip().split('\n')
        if lines:
            name = lines[0]
            ingredients = lines[1:]
            recipes.append((name, ingredients))

    recipes.sort(key=lambda x: x[0])

    with open(output_file, 'w') as file:
        for i, (name, ingredients) in enumerate(recipes):
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            if i < len(recipes) - 1:
                file.write('\n')