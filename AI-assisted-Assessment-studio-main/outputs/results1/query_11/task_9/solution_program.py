def calculate_total_cost(recipe_ingredients, ingredient_prices):
    price_dict = {}
    total_cost = 0.0
    for item in ingredient_prices.split(','):
        ingredient, price = item.split(':')
        price_dict[ingredient] = float(price)
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name, quantity = ingredient.split(':')
            cost = price_dict[name] * int(quantity)
            total_cost += cost
    return total_cost
