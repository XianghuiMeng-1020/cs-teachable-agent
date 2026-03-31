def calculate_total_cost(recipe_ingredients, ingredient_prices):
    total_cost = 0.0
    prices = {}

    for price in ingredient_prices:
        ingredient, cost = price.split(':')
        prices[ingredient] = float(cost)

    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name, quantity = ingredient.split(':')
            quantity = int(quantity)
            total_cost += prices[name] * quantity

    return total_cost