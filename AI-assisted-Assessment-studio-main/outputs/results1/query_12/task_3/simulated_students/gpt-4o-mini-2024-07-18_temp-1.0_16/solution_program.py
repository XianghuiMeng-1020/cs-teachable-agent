import os

def categorize_recipes(input_folder, output_file):
    results = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(input_folder, filename), 'r') as file:
                ingredients = file.readlines()
                num_ingredients = len(ingredients)
                category = 'simple' if num_ingredients <= 7 else 'complex'
                results.append(f'{filename}: {category}')
    with open(output_file, 'w') as out_file:
        out_file.write('\n'.join(results) + '\n')