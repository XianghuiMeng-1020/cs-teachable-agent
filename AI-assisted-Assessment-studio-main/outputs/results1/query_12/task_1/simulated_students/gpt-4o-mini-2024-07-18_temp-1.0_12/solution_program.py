import os


def estimate_cooking_times() -> None:
    recipe_dir = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []
    
    for filename in sorted(os.listdir(recipe_dir)):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6:-4]
            total_time = 0
            with open(os.path.join(recipe_dir, filename), 'r') as file:
                for line in file:
                    parts = line.split('-')
                    if len(parts) > 1:
                        time_part = parts[1].strip().split()[0]
                        total_time += int(time_part)
            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')
    
    with open(output_file, 'w') as out_file:
        for cooking_time in cooking_times:
            out_file.write(cooking_time + '\n')