import os

def estimate_cooking_times() -> None:
    recipe_directory = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    for filename in sorted(os.listdir(recipe_directory)):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = int(filename[6:-4])
            total_time = 0

            with open(os.path.join(recipe_directory, filename), 'r') as file:
                for line in file:
                    parts = line.split('-')
                    if len(parts) > 1:
                        time_part = parts[1].strip()  
                        minutes = int(time_part.split()[0])
                        total_time += minutes

            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(cooking_times) + '\n')