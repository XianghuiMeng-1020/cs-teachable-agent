def calculate_total_cost(recipe_ingredients, ingredient_prices):
    price_dict = {}
    total_cost = 0.0
    
    for price in ingredient_prices:
        name, cost = price.split(':')
        price_dict[name] = float(cost)
    
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name, quantity = ingredient.split(':')
            total_cost += price_dict[name] * int(quantity)
    
    return total_cost