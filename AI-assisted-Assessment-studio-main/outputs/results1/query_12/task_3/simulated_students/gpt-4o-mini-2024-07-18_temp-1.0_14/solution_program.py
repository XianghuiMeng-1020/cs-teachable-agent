import os

def categorize_recipes(input_folder, output_file):
    results = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(input_folder, filename)
            with open(filepath, 'r') as f:
                ingredients = f.readlines()
                num_ingredients = len(ingredients)
                if num_ingredients > 7:
                    results.append(f'{filename}: complex')
                else:
                    results.append(f'{filename}: simple')
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')