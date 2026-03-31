def calculate_total_cost(recipe_data, cost_data):
    total_cost = {}
    for dish, ingredients in recipe_data.items():
        cost = 0
        for ingredient, quantity in ingredients:
            if ingredient not in cost_data:
                raise ValueError(f"Cost information is missing for ingredient: {ingredient}")
            cost += cost_data[ingredient] * quantity
        total_cost[dish] = round(cost, 2)
    return total_cost