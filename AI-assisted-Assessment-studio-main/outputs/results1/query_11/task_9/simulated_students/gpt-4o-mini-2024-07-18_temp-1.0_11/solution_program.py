def calculate_total_cost(recipe_ingredients, ingredient_prices):
    price_map = {}
    total_cost = 0.0
    
    for price_entry in ingredient_prices:
        ingredient, price = price_entry.split(':')
        price_map[ingredient] = float(price)
    
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name, quantity = ingredient.split(':')
            quantity = int(quantity)
            cost = quantity * price_map[name]
            total_cost += cost
    
    return total_cost