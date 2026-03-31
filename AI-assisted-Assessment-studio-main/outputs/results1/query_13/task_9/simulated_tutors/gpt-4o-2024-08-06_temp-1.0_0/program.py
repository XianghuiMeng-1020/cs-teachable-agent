def calculate_ingredient_costs(filename, quantities):
    try:
        total_cost = 0
        with open(filename, 'r') as file:
            ingredient_prices = {}
            for line in file:
                name, price = line.strip().split(':')
                ingredient_prices[name.strip()] = float(price.strip())
            for ingredient, quantity in quantities.items():
                if ingredient in ingredient_prices:
                    total_cost += ingredient_prices[ingredient] * quantity
        return total_cost
    except FileNotFoundError:
        return None