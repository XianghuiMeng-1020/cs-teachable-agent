def calculate_total_cost(recipe_data, cost_data):
    total_costs = {}
    
    for dish, ingredients in recipe_data.items():
        total_cost = 0
        for ingredient, quantity in ingredients:
            if ingredient not in cost_data:
                raise ValueError(f"Cost information is missing for ingredient: {ingredient}")
            total_cost += cost_data[ingredient] * quantity
        total_costs[dish] = round(total_cost, 2)
    
    return total_costs