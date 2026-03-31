def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as recipes:
        recipes_lines = recipes.read().strip().split('\n')

    with open(available_file, 'r') as available:
        available_list = [item.strip().lower() for item in available.readlines()]

    missing_ingredients = []
    current_ingredients = []

    for line in recipes_lines:
        line = line.strip()
        if line == '':
            missing_ingredients.extend([item for item in current_ingredients if item.lower() not in available_list])
            current_ingredients = []
        else:
            if line.startswith(tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')):
                current_ingredients.append(line)

    missing_ingredients.extend([item for item in current_ingredients if item.lower() not in available_list])

    with open(output_file, 'w') as output:
        output.write('\n'.join(missing_ingredients))