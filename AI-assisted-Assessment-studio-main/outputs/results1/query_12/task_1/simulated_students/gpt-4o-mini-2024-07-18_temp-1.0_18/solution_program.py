import os


def estimate_cooking_times() -> None:
    recipe_dir = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    for filename in os.listdir(recipe_dir):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6:-4]  # Extracting number from filename
            total_time = 0
            with open(os.path.join(recipe_dir, filename), 'r') as file:
                for line in file:
                    parts = line.rsplit(' - ', 1)
                    if len(parts) == 2:
                        time_part = parts[1].strip()  # Get the time part
                        minutes = int(time_part.split()[0])  # Get integer minutes
                        total_time += minutes
            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open(output_file, 'w') as output:  
        for line in cooking_times:
            output.write(line + '\n')
