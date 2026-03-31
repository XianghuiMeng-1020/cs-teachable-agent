def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    recipes = content.strip().split('\n\n')
    sorted_recipes = []

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        if lines:
            recipe_name = lines[0]
            ingredients = lines[1:]
            sorted_recipes.append((recipe_name, ingredients))

    sorted_recipes.sort(key=lambda x: x[0])

    with open(output_file, 'w') as file:
        for recipe_name, ingredients in sorted_recipes:
            file.write(recipe_name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write('\n')