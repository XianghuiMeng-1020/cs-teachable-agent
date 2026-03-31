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
        for recipe in recipes:
            file.write(recipe[0] + '\n')
            for ingredient in recipe[1]:
                file.write(ingredient + '\n')
            file.write('\n')