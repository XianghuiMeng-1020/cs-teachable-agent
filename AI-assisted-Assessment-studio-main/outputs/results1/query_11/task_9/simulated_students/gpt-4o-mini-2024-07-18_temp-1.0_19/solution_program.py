def calculate_total_cost(recipe_ingredients, ingredient_prices):
    price_dict = {}
    total_cost = 0.0

    for price_entry in ingredient_prices:
        ingredient, price = price_entry.split(':')
        price_dict[ingredient] = float(price)

    for recipe in recipe_ingredients:
        ingredients = recipe.split(',')
        for ingredient in ingredients:
            name_quantity = ingredient.split(':')
            ingredient_name = name_quantity[0]
            quantity = int(name_quantity[1])
            total_cost += price_dict[ingredient_name] * quantity

    return total_cost