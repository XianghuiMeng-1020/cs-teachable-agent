import os


def estimate_cooking_times() -> None:
    recipes_dir = 'recipes/'
    cooking_times = []
    
    for filename in sorted(os.listdir(recipes_dir)):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6]  # Extract recipe number from filename
            total_time = 0
            with open(os.path.join(recipes_dir, filename), 'r') as file:
                for line in file:
                    # Extracting the time from the line
                    parts = line.split('-')
                    if len(parts) > 1:
                        time_part = parts[1].strip().split()[0]  # Get the number part before "minutes"
                        total_time += int(time_part)
            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open('cooking_times.txt', 'w') as output_file:
        output_file.write('\n'.join(cooking_times) + '\n')