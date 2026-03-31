def recipe_value(recipe, prices):
    # Convert prices list to a dictionary for quick lookup
    price_dict = {}
    for item in prices:
        ingredient, price = item.split(":")
        price_dict[ingredient] = float(price)

    # Calculate total cost based on recipe ingredients and prices
    total_cost = 0.0
    for item in recipe:
        ingredient, amount = item.split(":")
        amount = int(amount)
        # Get the price of the ingredient or 0 if not found
        price_per_unit = price_dict.get(ingredient, 0)
        total_cost += price_per_unit * amount

    return total_cost
