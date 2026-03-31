def calculate_total_cost(recipe_ingredients, ingredient_prices):
    prices_dict = {}
    total_cost = 0.0
    
    for price_entry in ingredient_prices:
        name, price = price_entry.split(':')
        prices_dict[name.strip()] = float(price.strip())
    
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name_quantity = ingredient.split(':')
            name = name_quantity[0].strip()
            quantity = int(name_quantity[1].strip())
            total_cost += prices_dict[name] * quantity
    
    return total_cost