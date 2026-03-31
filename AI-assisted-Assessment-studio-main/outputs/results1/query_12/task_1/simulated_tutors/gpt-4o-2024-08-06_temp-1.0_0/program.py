import os

def estimate_cooking_times() -> None:
    # Check if 'recipes/' directory exists
    if not os.path.isdir('recipes'):
        return

    cooking_times = []

    # Process each file in the 'recipes/' directory
    for filename in sorted(os.listdir('recipes')):
        # Ensure that the file follows the naming convention 'recipeX.txt'
        if filename.startswith('recipe') and filename.endswith('.txt'):
            # Extract the recipe number
            try:
                recipe_number = int(filename[len('recipe'):filename.index('.txt')])
            except ValueError:
                continue
    
            total_time = 0
            with open(os.path.join('recipes', filename), 'r') as f:
                for line in f:
                    # Extract the time from each step
                    try:
                        time_part = line.split('-')[-1].strip()
                        minutes = int(time_part.split()[0])
                        total_time += minutes
                    except (IndexError, ValueError):
                        continue

            cooking_times.append((recipe_number, total_time))
    
    # Write the results to 'cooking_times.txt'
    if cooking_times:
        with open('cooking_times.txt', 'w') as output_file:
            for recipe_number, total_time in sorted(cooking_times):
                output_file.write(f'Recipe {recipe_number}: {total_time} minutes\n')