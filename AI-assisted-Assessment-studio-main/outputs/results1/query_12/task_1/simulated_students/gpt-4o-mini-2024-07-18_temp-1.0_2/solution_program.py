import os


def estimate_cooking_times() -> None:
    recipe_dir = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    # Get a sorted list of recipe files in the directory
    recipe_files = sorted([f for f in os.listdir(recipe_dir) if f.startswith('recipe') and f.endswith('.txt')])

    # Process each recipe file
    for recipe_file in recipe_files:
        total_time = 0
        with open(os.path.join(recipe_dir, recipe_file), 'r') as file:
            for line in file:
                # Extract time from line
                parts = line.split('-')
                if len(parts) > 1:
                    time_part = parts[1].strip()
                    # Get the time in minutes
                    time_in_minutes = int(time_part.split()[0])
                    total_time += time_in_minutes

        recipe_number = recipe_file.replace('recipe', '').replace('.txt', '')
        cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    # Write results to cooking_times.txt
    with open(output_file, 'w') as output:
        for cooking_time in cooking_times:
            output.write(cooking_time + '\n')