def sort_ingredients(input_filename, output_filename):
    # Open the input file and output file
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            # Split the line into ingredients
            ingredients = line.strip().split(',')
            # Trim spaces and sort the ingredients
            sorted_ingredients = sorted(ingredient.strip() for ingredient in ingredients)
            # Join sorted ingredients and write to the output file
            outfile.write(', '.join(sorted_ingredients) + '\n')