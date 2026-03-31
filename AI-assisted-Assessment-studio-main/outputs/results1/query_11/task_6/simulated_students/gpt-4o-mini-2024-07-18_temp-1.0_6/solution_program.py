def recipe_value(recipe, prices):
    price_dict = {item.split(':')[0]: float(item.split(':')[1]) for item in prices}
    total_cost = 0.0
    for item in recipe:
        ingredient, amount = item.split(':')
        amount = int(amount)
        if ingredient in price_dict:
            total_cost += price_dict[ingredient] * amount
    return total_cost