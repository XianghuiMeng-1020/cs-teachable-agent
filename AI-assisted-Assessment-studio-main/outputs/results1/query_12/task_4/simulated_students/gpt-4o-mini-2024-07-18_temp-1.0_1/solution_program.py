def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read().strip()  

    recipes = content.split('\n\n')  
    recipe_list = []

    for recipe in recipes:
        lines = recipe.split('\n')
        if len(lines) > 0:
            name = lines[0]  
            ingredients = lines[1:]
            recipe_list.append((name, ingredients))

    recipe_list.sort(key=lambda x: x[0])

    with open(output_file, 'w') as outfile:
        for name, ingredients in recipe_list:
            outfile.write(name + '\n')
            for ingredient in ingredients:
                outfile.write(ingredient + '\n')
            outfile.write('\n')