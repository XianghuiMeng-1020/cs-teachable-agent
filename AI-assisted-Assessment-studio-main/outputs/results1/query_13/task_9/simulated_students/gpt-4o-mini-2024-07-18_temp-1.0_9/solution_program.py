def calculate_ingredient_costs(filename, quantities):
    try:
        with open(filename, 'r') as file:
            ingredient_costs = {}  
            for line in file:
                ingredient, cost = line.strip().split(':')
                ingredient_costs[ingredient] = float(cost)
    except IOError:
        return None

    total_cost = 0
    for ingredient, amount in quantities.items():
        if ingredient in ingredient_costs:
            total_cost += ingredient_costs[ingredient] * amount

    return total_cost