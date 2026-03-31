def calculate_total_ingredients(ingredient_list):
    ingredient_totals = {}

    for item in ingredient_list:
        try:
            # Split the string into ingredient and quantity
            ingredient, quantity = item.split(':')
            # Strip whitespace
            ingredient = ingredient.strip()
            quantity = quantity.strip()
            # Convert quantity to integer
            quantity = int(quantity)
            # Check if quantity is positive
            if quantity < 1:
                raise ValueError
        except (ValueError, TypeError):
            continue

        # Sum the quantities for each ingredient
        if ingredient in ingredient_totals:
            ingredient_totals[ingredient] += quantity
        else:
            ingredient_totals[ingredient] = quantity

    return ingredient_totals