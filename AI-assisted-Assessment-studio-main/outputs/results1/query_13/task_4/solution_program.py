def calculate_total_ingredients(ingredient_list):
    ingredient_totals = {}
    for entry in ingredient_list:
        try:
            ingredient, quantity = entry.split(':')
            if not ingredient or not quantity.isdigit():
                raise ValueError("Invalid entry format")
            quantity = int(quantity)
            if ingredient in ingredient_totals:
                ingredient_totals[ingredient] += quantity
            else:
                ingredient_totals[ingredient] = quantity
        except ValueError:
            continue
    return ingredient_totals