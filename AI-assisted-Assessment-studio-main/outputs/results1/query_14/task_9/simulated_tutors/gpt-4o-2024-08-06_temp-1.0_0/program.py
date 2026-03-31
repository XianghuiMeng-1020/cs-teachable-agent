def parse_ingredient_list(ingredient_string):
    # Initialize an empty dictionary to store ingredient name and quantity pairs
    ingredients_dict = {}
    
    # Split the input string on semicolons to separate each ingredient-quantity pair
    if ingredient_string:
        ingredient_entries = ingredient_string.split(';')

        # Iterate over each ingredient-quantity pair
        for entry in ingredient_entries:
            # Split each entry on colon to separate the ingredient name and quantity
            if ':' in entry:
                name, quantity = entry.split(':', 1)
                # Add the name and quantity to the dictionary
                ingredients_dict[name] = quantity

    return ingredients_dict