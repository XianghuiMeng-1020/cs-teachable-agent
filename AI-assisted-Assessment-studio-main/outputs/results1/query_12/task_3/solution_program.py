import os

def categorize_recipes(input_folder, output_file):
    recipe_files = os.listdir(input_folder)
    results = []
    for recipe_file in recipe_files:
        with open(os.path.join(input_folder, recipe_file), 'r') as file:
            ingredients_count = sum(1 for _ in file)
            category = 'complex' if ingredients_count > 7 else 'simple'
            results.append(f"{recipe_file}: {category}")
    with open(output_file, 'w') as output:
        for result in results:
            output.write(f"{result}\n")