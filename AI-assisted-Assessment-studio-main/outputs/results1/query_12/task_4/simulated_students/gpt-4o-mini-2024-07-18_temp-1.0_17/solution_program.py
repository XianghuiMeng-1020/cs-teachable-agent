def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read().strip()  

    recipes = content.split('\n\n')
    sorted_recipes = []

    for recipe in recipes:
        if recipe.strip():
            sorted_recipes.append(recipe.strip())

    sorted_recipes.sort()  

    with open(output_file, 'w') as file:
        for i, recipe in enumerate(sorted_recipes):
            file.write(recipe)
            if i < len(sorted_recipes) - 1:
                file.write('\n\n')