import os


def estimate_cooking_times() -> None:
    # Output file
    output_file = 'cooking_times.txt'
    # Open output file
    with open(output_file, 'w') as outf:
        # Loop through all recipe files in 'recipes/' directory
        for filename in sorted(os.listdir('recipes/')):
            if filename.startswith('recipe') and filename.endswith('.txt'):
                recipe_number = filename[6:-4]  # Extract the recipe number
                total_time = 0
                # Open the recipe file
                with open(os.path.join('recipes/', filename), 'r') as rf:
                    for line in rf:
                        # Extract time from the line
                        parts = line.split('-')
                        if len(parts) > 1:
                            time_part = parts[1].strip()
                            # Get the numeric time value
                            if 'minutes' in time_part:
                                time_value = int(time_part.split()[0])
                                total_time += time_value
                # Write the total cooking time to the output file
                outf.write(f'Recipe {recipe_number}: {total_time} minutes\n')