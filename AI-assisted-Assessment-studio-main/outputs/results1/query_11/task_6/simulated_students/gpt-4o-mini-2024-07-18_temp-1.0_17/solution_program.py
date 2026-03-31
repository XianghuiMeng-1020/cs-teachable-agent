def recipe_value(recipe, prices):
    price_dict = {}
    total_cost = 0.0

    for item in prices:
        ingredient, price_per_unit = item.split(':')
        price_dict[ingredient] = float(price_per_unit)

    for item in recipe:
        ingredient, amount = item.split(':')
        amount = int(amount)
        # If the ingredient has a price, add to total cost, else add 0
        total_cost += price_dict.get(ingredient, 0) * amount

    return total_cost