def parse_ingredient_list(ingredient_str):
    # Prepare a dictionary to store the parsed ingredients
    ingredients = {}

    # Split the incoming string by semicolons to separate individual ingredients
    ingredient_list = ingredient_str.split(';')

    for item in ingredient_list:
        # Strip any extra whitespace and split by comma
        parts = [part.strip() for part in item.split(',')]
        # Extracting ingredient name, quantity, and unit
        if len(parts) == 3:
            ingredient_name = parts[0]
            quantity = parts[1]
            unit = parts[2]
            # Storing the data in the dictionary
            ingredients[ingredient_name] = {'quantity': quantity, 'unit': unit}

    return ingredients