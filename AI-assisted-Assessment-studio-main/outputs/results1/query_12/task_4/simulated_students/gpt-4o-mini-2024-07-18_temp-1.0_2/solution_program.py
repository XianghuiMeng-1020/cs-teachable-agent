def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read().strip()  
    recipes = content.split('\n\n')
    recipe_list = []
    
    for recipe in recipes:
        lines = recipe.strip().split('\n')
        recipe_name = lines[0]
        ingredients = lines[1:]
        recipe_list.append((recipe_name, ingredients))
    
    recipe_list.sort(key=lambda x: x[0])
    
    with open(output_file, 'w') as outfile:
        for recipe_name, ingredients in recipe_list:
            outfile.write(recipe_name + '\n')
            outfile.write('\n'.join(ingredients) + '\n\n')