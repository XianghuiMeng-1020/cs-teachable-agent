def calculate_ingredient_costs(filename, quantities):
    total_cost = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                name, cost = line.strip().split(':')
                if name in quantities:
                    total_cost += float(cost) * quantities[name]
    except:
        return None
    return total_cost