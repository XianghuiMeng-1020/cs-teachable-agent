import os

def categorize_recipes(input_folder, output_file):
    with open(output_file, 'w') as outfile:
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
                    outfile.write(f'{filename}: {category}\n')