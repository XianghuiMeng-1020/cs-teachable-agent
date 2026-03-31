import os


def estimate_cooking_times() -> None:
    directory = 'recipes/'
    output_file = 'cooking_times.txt'
    cooking_times = []

    # Iterate through all recipe files in the specified directory
    for filename in sorted(os.listdir(directory)):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6:-4]  # Extracting the recipe number
            total_time = 0

            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    parts = line.split(' - ')
                    if len(parts) > 1:
                        time_str = parts[1].strip().split(' ')[0]  # Extracting time
                        total_time += int(time_str)

            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    # Write the results to the output file
    with open(output_file, 'w') as outfile:
        for line in cooking_times:
            outfile.write(line + '\n')