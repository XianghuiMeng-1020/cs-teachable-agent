import os

def categorize_recipes(input_folder, output_file):
    with open(output_file, 'w') as output:
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r') as file:
                    ingredients = file.readlines()
                    count = len(ingredients)
                    if count > 7:
                        category = 'complex'
                    else:
                        category = 'simple'
                    output.write(f"{filename}: {category}\n")