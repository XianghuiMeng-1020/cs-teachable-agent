def recipe_summary(recipe):
    # Initialize an empty dictionary to store the summary
    summary = {}
    
    # Split the input string into lines
    lines = recipe.strip().split('\n')
    
    # Process each line
    for line in lines:
        # Split each line by the first occurrence of ':' to get ingredient, quantity and unit
        ingredient, rest = line.split(':')
        quantity, unit = rest.strip().split(' ', 1)
        
        # Add the parsed ingredient information to the dictionary
        summary[ingredient.strip()] = {
            'quantity': quantity,
            'unit': unit
        }
    
    return summary