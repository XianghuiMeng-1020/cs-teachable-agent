def calculate_ingredient_costs(filename, quantities):
    try:
        with open(filename, 'r') as file:
            prices = {}
            for line in file:
                ingredient, cost = line.strip().split(':')
                prices[ingredient] = float(cost)
    except IOError:
        return None

    total_cost = 0.0
    for ingredient, quantity in quantities.items():
        if ingredient in prices:
            total_cost += prices[ingredient] * quantity

    return total_cost