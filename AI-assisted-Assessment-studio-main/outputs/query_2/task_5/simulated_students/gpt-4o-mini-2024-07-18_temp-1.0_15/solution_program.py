def sort_ingredients(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    sorted_lines = []
    for line in lines:
        ingredients = line.split(',')
        ingredients = [ingredient.strip() for ingredient in ingredients]
        ingredients.sort()
        sorted_line = ', '.join(ingredients)
        sorted_lines.append(sorted_line)

    with open(output_filename, 'w') as outfile:
        for sorted_line in sorted_lines:
            outfile.write(sorted_line + '\n')