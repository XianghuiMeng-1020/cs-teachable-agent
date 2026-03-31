def sort_ingredients(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    sorted_lines = []
    for line in lines:
        ingredients = line.strip().split(',')
        sorted_ingredients = sorted([ingredient.strip() for ingredient in ingredients])
        sorted_lines.append(', '.join(sorted_ingredients))

    with open(output_filename, 'w') as outfile:
        outfile.write('\n'.join(sorted_lines))