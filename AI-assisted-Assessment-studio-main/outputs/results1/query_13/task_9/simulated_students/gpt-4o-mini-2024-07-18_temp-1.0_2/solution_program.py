def calculate_ingredient_costs(filename, quantities):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except:
        return None

    ingredient_costs = {}
    for line in lines:
        ingredient, cost = line.strip().split(':')
        ingredient_costs[ingredient] = float(cost)

    total_cost = 0
    for ingredient, quantity in quantities.items():
        if ingredient in ingredient_costs:
            total_cost += ingredient_costs[ingredient] * quantity

    return total_cost