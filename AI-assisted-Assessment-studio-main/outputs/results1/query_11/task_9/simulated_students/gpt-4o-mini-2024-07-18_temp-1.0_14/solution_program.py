def calculate_total_cost(recipe_ingredients, ingredient_prices):
    price_dict = {}
    for price_entry in ingredient_prices:
        ingredient, price = price_entry.split(':')
        price_dict[ingredient] = float(price)
    total_cost = 0.0
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name, quantity = ingredient.split(':')
            quantity = int(quantity)
            total_cost += price_dict[name] * quantity
    return total_cost