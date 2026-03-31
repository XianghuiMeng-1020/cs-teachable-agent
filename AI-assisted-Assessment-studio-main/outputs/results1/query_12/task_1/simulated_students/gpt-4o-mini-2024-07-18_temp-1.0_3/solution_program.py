import os


def estimate_cooking_times() -> None:
    recipe_dir = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    for filename in sorted(os.listdir(recipe_dir)):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_index = filename[6:-4]  # Extracting the recipe number
            total_time = 0
            with open(os.path.join(recipe_dir, filename), 'r') as file:
                for line in file:
                    parts = line.split('-')
                    if len(parts) > 1:
                        time_part = parts[1].strip()
                        if 'minutes' in time_part:
                            time_value = int(time_part.split()[0])
                            total_time += time_value
            cooking_times.append(f'Recipe {recipe_index}: {total_time} minutes')

    with open(output_file, 'w') as output:
        for line in cooking_times:
            output.write(line + '\n')