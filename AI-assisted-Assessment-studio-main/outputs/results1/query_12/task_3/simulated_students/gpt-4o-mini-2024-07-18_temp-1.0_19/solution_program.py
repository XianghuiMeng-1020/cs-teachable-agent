import os

def categorize_recipes(input_folder, output_file):
    results = []
    for recipe_file in os.listdir(input_folder):
        if recipe_file.endswith('.txt'):
            with open(os.path.join(input_folder, recipe_file), 'r') as f:
                ingredients = f.readlines()
                ingredient_count = len(ingredients)
                if ingredient_count > 7:
                    category = 'complex'
                else:
                    category = 'simple'
                results.append(f'{recipe_file}: {category}')
    with open(output_file, 'w') as f:
        f.write('\n'.join(results))