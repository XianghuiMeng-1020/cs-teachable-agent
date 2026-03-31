def calculate_total_cost(recipe_ingredients, ingredient_prices):
    prices = {}
    total_cost = 0.0

    for price_entry in ingredient_prices:
        ingredient, price = price_entry.split(':')
        prices[ingredient] = float(price)

    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name, quantity = ingredient.split(':')
            quantity = int(quantity)
            total_cost += prices[name] * quantity

    return total_cost