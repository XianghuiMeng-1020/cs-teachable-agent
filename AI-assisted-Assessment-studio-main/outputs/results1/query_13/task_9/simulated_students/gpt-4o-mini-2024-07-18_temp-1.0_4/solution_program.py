def calculate_ingredient_costs(filename, quantities):
    try:
        with open(filename, 'r') as file:
            costs = {}
            for line in file:
                ingredient, cost = line.strip().split(':')
                costs[ingredient] = float(cost)
    except:
        return None

    total_cost = 0
    for ingredient, amount in quantities.items():
        if ingredient in costs:
            total_cost += costs[ingredient] * amount

    return total_cost