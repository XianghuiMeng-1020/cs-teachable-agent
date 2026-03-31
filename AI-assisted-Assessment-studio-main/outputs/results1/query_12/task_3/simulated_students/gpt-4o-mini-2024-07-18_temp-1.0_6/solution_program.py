import os

def categorize_recipes(input_folder, output_file):
    results = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as file:
                ingredients = file.readlines()
                ingredient_count = len(ingredients)
                if ingredient_count > 7:
                    category = 'complex'
                else:
                    category = 'simple'
                results.append(f'{filename}: {category}')
    with open(output_file, 'w') as output:
        for result in results:
            output.write(result + '\n')