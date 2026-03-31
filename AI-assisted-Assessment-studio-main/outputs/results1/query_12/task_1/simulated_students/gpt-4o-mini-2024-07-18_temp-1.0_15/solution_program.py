import os


def estimate_cooking_times() -> None:
    recipe_folder = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    for filename in sorted(os.listdir(recipe_folder)):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6:-4]  # Extract number from filename
            total_time = 0
            with open(os.path.join(recipe_folder, filename), 'r') as file:
                for line in file:
                    parts = line.rsplit(' - ', 1)
                    if len(parts) == 2:
                        time_str = parts[1].strip()
                        if 'minutes' in time_str:
                            minutes = int(time_str.split()[0])
                            total_time += minutes
            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open(output_file, 'w') as out_file:
        for line in cooking_times:
            out_file.write(line + '\n')
