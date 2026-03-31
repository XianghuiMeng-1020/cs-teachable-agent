def calculate_total_cost(recipe_ingredients, ingredient_prices):
    # Convert ingredient prices into a dictionary for easy lookup
    price_dict = {}
    for price_entry in ingredient_prices:
        ingredient, price = price_entry.split(':')
        price_dict[ingredient] = float(price)
    
    total_cost = 0.0
    # Process each recipe
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient_entry in ingredients:
            ingredient_name, quantity_str = ingredient_entry.split(':')
            quantity = int(quantity_str)
            # Calculate cost for this ingredient
            if ingredient_name in price_dict:
                total_cost += price_dict[ingredient_name] * quantity
    
    return total_cost