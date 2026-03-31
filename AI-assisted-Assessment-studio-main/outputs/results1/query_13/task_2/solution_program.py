def calculate_total_cost(recipe_data, cost_data):
    total_costs = {}
    for dish, ingredients in recipe_data.items():
        total_cost = 0
        for ingredient, quantity in ingredients:
            if ingredient not in cost_data:
                raise ValueError(f"Cost information missing for: {ingredient}")
            total_cost += cost_data[ingredient] * quantity
        total_costs[dish] = total_cost
    return total_costs