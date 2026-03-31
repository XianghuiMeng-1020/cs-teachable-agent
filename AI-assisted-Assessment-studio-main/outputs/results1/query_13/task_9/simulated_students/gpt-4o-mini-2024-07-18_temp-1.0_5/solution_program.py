def calculate_ingredient_costs(filename, quantities):
    try:
        with open(filename, 'r') as file:
            cost_data = file.readlines()
    except IOError:
        return None

    cost_dict = {}
    for line in cost_data:
        ingredient, cost = line.strip().split(':')
        cost_dict[ingredient] = float(cost)

    total_cost = 0.0
    for ingredient, quantity in quantities.items():
        if ingredient in cost_dict:
            total_cost += cost_dict[ingredient] * quantity

    return total_cost