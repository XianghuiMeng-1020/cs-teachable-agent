import os


def estimate_cooking_times() -> None:
    recipe_directory = 'recipes/'
    cooking_times = []

    for filename in os.listdir(recipe_directory):
        if filename.startswith('recipe') and filename.endswith('.txt'):
            recipe_number = filename[6:-4]  # Extract the recipe number
            total_time = 0

            with open(os.path.join(recipe_directory, filename), 'r') as file:
                for line in file:
                    parts = line.strip().split(' - ')
                    if len(parts) == 2:
                        time_part = parts[1].strip()  # Get the time part
                        time_in_minutes = int(time_part.split(' ')[0])  # Convert minutes to int
                        total_time += time_in_minutes

            cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open('cooking_times.txt', 'w') as output_file:
        for line in cooking_times:
            output_file.write(line + '\n')