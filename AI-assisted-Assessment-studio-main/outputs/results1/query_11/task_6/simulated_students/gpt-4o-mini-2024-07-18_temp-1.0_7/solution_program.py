def recipe_value(recipe, prices):
    price_dict = {}
    
    for price in prices:
        ingredient, cost = price.split(':')
        price_dict[ingredient] = float(cost)
    
    total_cost = 0.0
    
    for item in recipe:
        ingredient, amount = item.split(':')
        amount = int(amount)
        total_cost += price_dict.get(ingredient, 0) * amount
    
    return total_cost