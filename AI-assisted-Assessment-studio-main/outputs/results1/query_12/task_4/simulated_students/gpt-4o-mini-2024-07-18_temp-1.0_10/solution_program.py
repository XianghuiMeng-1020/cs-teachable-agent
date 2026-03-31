def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read().strip()  
        recipes = content.split('\n\n')  

    sorted_recipes = []
    for recipe in recipes:
        lines = recipe.strip().split('\n')
        sorted_recipes.append(lines)

    sorted_recipes.sort(key=lambda x: x[0])

    with open(output_file, 'w') as outfile:
        for recipe in sorted_recipes:
            outfile.write('\n'.join(recipe) + '\n\n')
