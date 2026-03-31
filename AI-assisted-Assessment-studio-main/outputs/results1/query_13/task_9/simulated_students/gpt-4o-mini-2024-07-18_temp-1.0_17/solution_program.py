def calculate_ingredient_costs(filename, quantities):
    try:
        with open(filename, 'r') as file:
            ingredient_costs = {line.split(':')[0]: float(line.split(':')[1]) for line in file}
    except:
        return None

    total_cost = 0
    for ingredient, quantity in quantities.items():
        if ingredient in ingredient_costs:
            total_cost += ingredient_costs[ingredient] * quantity

    return total_cost