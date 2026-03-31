import os

def categorize_recipes(input_folder, output_file):
    results = []
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, 'r') as file:
                ingredients = file.readlines()
                num_ingredients = len(ingredients)
                if num_ingredients > 7:
                    category = 'complex'
                else:
                    category = 'simple'
                results.append(f'{filename}: {category}')
    
    with open(output_file, 'w') as out_file:
        for result in results:
            out_file.write(result + '\n')