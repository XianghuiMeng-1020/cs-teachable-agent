def recipe_value(recipe, prices):
    price_lookup = {}
    for entry in prices:
        ingredient, price = entry.split(':')
        price_lookup[ingredient] = float(price)
    total_cost = 0.0
    for item in recipe:
        ingredient, amount = item.split(':')
        if ingredient in price_lookup:
            total_cost += price_lookup[ingredient] * int(amount)
    return total_cost