import os

def categorize_recipes(input_folder, output_file):
    result = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, 'r') as file:
                ingredients = file.readlines()
                count = len(ingredients)
                if count > 7:
                    category = 'complex'
                else:
                    category = 'simple'
                result.append(f'{filename}: {category}')
    with open(output_file, 'w') as file:
        file.write('\n'.join(result))