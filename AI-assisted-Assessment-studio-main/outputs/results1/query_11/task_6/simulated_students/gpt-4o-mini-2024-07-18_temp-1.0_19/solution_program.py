def recipe_value(recipe, prices):
    price_dict = {}  
    total_cost = 0.0
    
    for price in prices:
        ingredient, cost = price.split(':')
        price_dict[ingredient] = float(cost)
    
    for item in recipe:
        ingredient, amount = item.split(':')
        amount = int(amount)
        cost_per_unit = price_dict.get(ingredient, 0)
        total_cost += cost_per_unit * amount
    
    return total_cost