def generate_ingredient_report():
    # Dictionary to keep count of each ingredient
    ingredient_count = {}
    
    try:
        # Open the recipes file if it exists
        with open('recipes.txt', 'r') as file:
            for line in file:
                # Strip any whitespace around the line
                line = line.strip()
                
                # Check for proper recipe format
                if ' | ' in line:
                    recipe_name, ingredients_part = line.split(' | ', 1)
                    ingredients = ingredients_part.split(', ')

                    # Count each ingredient
                    for ingredient in ingredients:
                        if ingredient in ingredient_count:
                            ingredient_count[ingredient] += 1
                        else:
                            ingredient_count[ingredient] = 1

    except FileNotFoundError:
        pass  # If the file does not exist, we'll just create an empty report

    # Sort the ingredients by count, descending
    sorted_ingredient_list = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)

    # Write the results to the output file
    with open('ingredient_report.txt', 'w') as output_file:
        for ingredient, count in sorted_ingredient_list:
            output_file.write(f'{ingredient}: {count}\n')