def suggest_recipe(budget, recipes):
    optimal_recipe = None
    closest_cost = -1

    for recipe in recipes:
        name, costs = recipe.split(':')
        total_cost = sum(map(int, costs.split(',')))

        if total_cost <= budget and total_cost > closest_cost:
            closest_cost = total_cost
            optimal_recipe = name

    return optimal_recipe if optimal_recipe else 'No recipe available'