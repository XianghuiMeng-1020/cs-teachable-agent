def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    recipes = content.strip().split('\n\n')
    recipe_list = []

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        if lines:
            recipe_name = lines[0]
            ingredients = lines[1:]
            recipe_list.append((recipe_name, ingredients))

    recipe_list.sort(key=lambda x: x[0])

    with open(output_file, 'w') as file:
        for recipe_name, ingredients in recipe_list:
            file.write(recipe_name + '\n')
            for i in range(0, len(ingredients), 2):
                file.write(ingredients[i] + '\n')
                file.write(ingredients[i + 1] + '\n')
            file.write('\n')