def calculate_total_ingredients(ingredient_list):
    ingredient_summary = {}
    for item in ingredient_list:
        try:
            ingredient, quantity = item.split(':')
            quantity = int(quantity)  # Ensure quantity is a positive integer
            # Sum the quantity for each ingredient
            if ingredient in ingredient_summary:
                ingredient_summary[ingredient] += quantity
            else:
                ingredient_summary[ingredient] = quantity
        except (ValueError, IndexError):
            # Skip items that cause exceptions due to improper format or conversion
            continue
    return ingredient_summary