import os


def estimate_cooking_times() -> None:
    recipe_dir = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    recipe_files = sorted(os.listdir(recipe_dir), key=lambda x: int(x.replace('recipe', '').replace('.txt', '')))

    for recipe_file in recipe_files:
        total_time = 0
        with open(os.path.join(recipe_dir, recipe_file), 'r') as file:
            for line in file:
                if '-' in line:
                    parts = line.split('-')
                    if len(parts) > 1:
                        time_part = parts[1].strip()
                        if time_part.endswith('minutes'):
                            time_value = int(time_part.replace('minutes', '').strip())
                            total_time += time_value
        recipe_num = int(recipe_file.replace('recipe', '').replace('.txt', ''))
        cooking_times.append(f'Recipe {recipe_num}: {total_time} minutes')

    with open(output_file, 'w') as output:
        output.write('\n'.join(cooking_times) + '\n')
