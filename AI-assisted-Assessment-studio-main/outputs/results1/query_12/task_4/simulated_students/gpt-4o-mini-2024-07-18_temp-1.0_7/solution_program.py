def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as file:
        data = file.read()

    recipes = data.strip().split('\n\n')
    recipe_list = []

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        recipe_name = lines[0]
        ingredients = lines[1:]
        recipe_list.append((recipe_name, ingredients))

    sorted_recipes = sorted(recipe_list, key=lambda x: x[0])

    with open(output_file, 'w') as file:
        for recipe_name, ingredients in sorted_recipes:
            file.write(recipe_name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write('\n')