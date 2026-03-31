def calculate_total_cost(recipe_ingredients, ingredient_prices):
    prices_dict = {}
    for price_entry in ingredient_prices:
        ingredient, price = price_entry.split(':')
        prices_dict[ingredient] = float(price)

    total_cost = 0.0
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name_quantity = ingredient.split(':')
            name = name_quantity[0]
            quantity = int(name_quantity[1])
            total_cost += prices_dict[name] * quantity

    return total_cost