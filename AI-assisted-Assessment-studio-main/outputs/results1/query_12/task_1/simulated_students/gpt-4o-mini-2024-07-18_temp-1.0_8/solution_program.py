import os


def estimate_cooking_times() -> None:
    recipe_folder = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    for filename in sorted(os.listdir(recipe_folder)):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6:-4]
            total_time = 0
            with open(os.path.join(recipe_folder, filename), 'r') as file:
                for line in file:
                    if '-' in line:
                        time_part = line.split('-')[-1].strip()
                        if 'minutes' in time_part:
                            time_value = time_part.split()[0]
                            total_time += int(time_value)
            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open(output_file, 'w') as output:
        for cooking_time in cooking_times:
            output.write(cooking_time + '\n')
