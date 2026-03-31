def suggest_recipe(budget, recipes):
    optimal_recipe = None
    closest_cost = -1

    for recipe in recipes:
        name, costs_str = recipe.split(':')
        ingredient_costs = list(map(int, costs_str.split(',')))
        total_cost = sum(ingredient_costs)

        if total_cost <= budget:
            if total_cost > closest_cost:
                closest_cost = total_cost
                optimal_recipe = name

    return optimal_recipe if optimal_recipe else 'No recipe available'