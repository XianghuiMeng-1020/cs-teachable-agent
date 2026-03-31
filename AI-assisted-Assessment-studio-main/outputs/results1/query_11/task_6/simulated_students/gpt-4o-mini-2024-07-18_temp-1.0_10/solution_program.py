def recipe_value(recipe, prices):
    price_dict = {}
    for price in prices:
        ingredient, unit_price = price.split(':')
        price_dict[ingredient] = float(unit_price)

    total_cost = 0.0
    for item in recipe:
        ingredient, amount = item.split(':')
        amount = int(amount)
        if ingredient in price_dict:
            total_cost += price_dict[ingredient] * amount

    return total_cost