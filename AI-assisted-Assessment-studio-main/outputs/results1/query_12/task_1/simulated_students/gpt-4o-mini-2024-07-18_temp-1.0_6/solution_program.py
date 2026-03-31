import os


def estimate_cooking_times() -> None:
    recipe_dir = 'recipes/'
    cooking_times_file = 'cooking_times.txt'
    results = []

    for filename in os.listdir(recipe_dir):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6:-4]  
            total_time = 0
            with open(os.path.join(recipe_dir, filename), 'r') as file:
                for line in file:
                    parts = line.rsplit(' - ', 1)
                    if len(parts) == 2:
                        time_str = parts[1].strip()
                        if time_str.endswith('minutes'):
                            time_value = int(time_str[:-8].strip())
                            total_time += time_value
            results.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open(cooking_times_file, 'w') as output_file:
        output_file.write('\n'.join(results) + '\n')
