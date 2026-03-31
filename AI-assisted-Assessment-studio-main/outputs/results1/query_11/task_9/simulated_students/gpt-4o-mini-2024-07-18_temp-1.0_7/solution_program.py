def calculate_total_cost(recipe_ingredients, ingredient_prices):
    price_dict = {}
    for ingredient in ingredient_prices:
        name, price = ingredient.split(':')
        price_dict[name] = float(price)

    total_cost = 0.0
    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for item in ingredients:
            name, quantity = item.split(':')
            quantity = int(quantity)
            total_cost += price_dict[name] * quantity

    return total_cost