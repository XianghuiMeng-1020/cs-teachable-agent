import os


def estimate_cooking_times() -> None:
    total_cooking_times = []
    recipe_dir = 'recipes/'
    recipe_files = sorted(os.listdir(recipe_dir), key=lambda x: int(x.replace('recipe', '').replace('.txt', '')))

    for recipe_file in recipe_files:
        total_time = 0
        with open(os.path.join(recipe_dir, recipe_file), 'r') as file:
            for line in file:
                if '-' in line:
                    # Extract the time from the line
                    time_part = line.split('-')[-1].strip()
                    # Expecting the format "T minutes"
                    if time_part.endswith('minutes'):
                        minutes = int(time_part.replace('minutes', '').strip())
                        total_time += minutes

        recipe_number = recipe_file.replace('recipe', '').replace('.txt', '')
        total_cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open('cooking_times.txt', 'w') as output_file:
        for cooking_time in total_cooking_times:
            output_file.write(cooking_time + '\n')
