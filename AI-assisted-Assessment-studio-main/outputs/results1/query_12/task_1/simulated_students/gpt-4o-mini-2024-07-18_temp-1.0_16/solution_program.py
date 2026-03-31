import os


def estimate_cooking_times() -> None:
    recipes_dir = 'recipes/'
    cooking_times = []
    recipe_files = sorted([f for f in os.listdir(recipes_dir) if f.startswith('recipe') and f.endswith('.txt')],
                         key=lambda x: int(x[6:-4]))  # sort by recipe number

    for recipe_file in recipe_files:
        total_time = 0
        with open(os.path.join(recipes_dir, recipe_file), 'r') as file:
            for line in file:
                parts = line.split('-')
                if len(parts) > 1:
                    time_str = parts[1].strip()  # Get the time part
                    minutes = int(time_str.split()[0])  # Extract only the integer part before 'minutes'
                    total_time += minutes
        recipe_number = recipe_file[6:-4]  # Extract the recipe number
        cooking_times.append(f'Recipe {recipe_number}: {total_time} minutes')

    with open('cooking_times.txt', 'w') as output_file:
        output_file.write('\n'.join(cooking_times))
