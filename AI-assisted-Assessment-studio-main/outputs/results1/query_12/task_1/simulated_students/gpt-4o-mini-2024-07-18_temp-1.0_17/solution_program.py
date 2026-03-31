import os


def estimate_cooking_times() -> None:
    recipe_directory = 'recipes/'
    cooking_times = []
    recipe_files = sorted([f for f in os.listdir(recipe_directory) if f.startswith('recipe') and f.endswith('.txt')], key=lambda x: int(x[6:-4]))

    for recipe_file in recipe_files:
        total_time = 0
        with open(os.path.join(recipe_directory, recipe_file), 'r') as file:
            for line in file:
                parts = line.split('-')
                if len(parts) > 1:
                    time_part = parts[1].strip()
                    time_value = int(time_part.split(' ')[0])  # extract the number before 'minutes'
                    total_time += time_value
        recipe_number = recipe_file[6:-4]  # Extracting the recipe number from filename
        cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open('cooking_times.txt', 'w') as output_file:
        output_file.write('\n'.join(cooking_times) + '\n')