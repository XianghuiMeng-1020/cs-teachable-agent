def recipe_value(recipe, prices):
    price_dict = {}
    for price in prices:
        ingredient, price_per_unit = price.split(':')
        price_dict[ingredient] = float(price_per_unit)

    total_cost = 0.0
    for item in recipe:
        ingredient, amount = item.split(':')
        amount = int(amount)
        total_cost += price_dict.get(ingredient, 0) * amount

    return total_cost