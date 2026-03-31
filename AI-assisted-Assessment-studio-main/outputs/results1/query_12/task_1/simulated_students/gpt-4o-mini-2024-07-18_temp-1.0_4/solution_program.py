import os

def estimate_cooking_times() -> None:
    file_path = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []
    
    for file_name in sorted(os.listdir(file_path)):
        if file_name.startswith('recipe') and file_name.endswith('.txt'):
            total_time = 0
            with open(os.path.join(file_path, file_name), 'r') as file:
                for line in file:
                    parts = line.split('-')
                    if len(parts) > 1:
                        time_part = parts[1].strip()
                        if 'minutes' in time_part:
                            time_value = int(time_part.split()[0])
                            total_time += time_value
            recipe_number = file_name[6:-4]  # Get the number part from 'recipeX.txt'
            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open(output_file, 'w') as output:
        for line in cooking_times:
            output.write(line + '\n')