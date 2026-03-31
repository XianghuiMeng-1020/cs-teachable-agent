def calculate_total_cost(recipe_data, cost_data):
    total_costs = {}
    
    for dish, ingredients in recipe_data.items():
        cost = 0.0
        for ingredient, quantity in ingredients:
            if ingredient not in cost_data:
                raise ValueError(f"Cost information missing for: {ingredient}")
            cost += cost_data[ingredient] * quantity
        total_costs[dish] = cost
    
    return total_costs

# Example usage
recipe_data = {
    "Pancake": [("Flour", 2), ("Egg", 3), ("Milk", 1)],
    "Omelette": [("Egg", 4), ("Milk", 2)]
}
cost_data = {
    "Flour": 0.5,
    "Egg": 0.2,
    "Milk": 1.0
}

result = calculate_total_cost(recipe_data, cost_data)
print(result)  # Output should be: {'Pancake': 2.6, 'Omelette': 1.4}