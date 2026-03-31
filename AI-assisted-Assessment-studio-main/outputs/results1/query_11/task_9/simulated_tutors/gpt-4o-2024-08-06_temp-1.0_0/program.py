def calculate_total_cost(recipe_ingredients, ingredient_prices):
    # Create a dictionary for ingredient prices
    price_dict = {}
    for item in ingredient_prices.split(','):
        name, price = item.split(':')
        price_dict[name] = float(price)
    
    total_cost = 0.0
    
    # Calculate total cost of ingredients
    for recipe in recipe_ingredients:
        for ingredient in recipe.split(','):
            name, quantity = ingredient.split(':')
            total_cost += price_dict[name] * int(quantity)
    
    return total_cost

# Example usage
recipes = ['flour:2,sugar:1','milk:3']
prices = 'flour:0.5,sugar:0.2,milk:1.0'
print(calculate_total_cost(recipes, prices))  # Should output 4.4