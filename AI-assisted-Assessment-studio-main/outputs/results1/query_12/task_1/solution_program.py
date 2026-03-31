import os

def estimate_cooking_times():
    output_filename = 'cooking_times.txt'
    recipe_path = 'recipes/'
    files = sorted([f for f in os.listdir(recipe_path) if f.startswith('recipe') and f.endswith('.txt')])
    with open(output_filename, 'w') as output_file:
        for file in files:
            total_minutes = 0
            with open(os.path.join(recipe_path, file), 'r') as recipe_file:
                for line in recipe_file:
                    parts = line.split('-')
                    if len(parts) == 2:
                        time_part = parts[1].strip().split()[0]
                        try:
                            total_minutes += int(time_part)
                        except ValueError:
                            pass
            recipe_number = file[len('recipe'):-len('.txt')]
            output_file.write(f'Recipe {recipe_number}: {total_minutes} minutes\n')