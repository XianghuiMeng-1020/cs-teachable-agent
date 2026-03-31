def suggest_recipe(budget, recipes):
    best_recipe = 'No recipe available'
    closest_cost = 0

    for recipe in recipes:
        name, costs = recipe.split(':')
        ingredient_costs = list(map(int, costs.split(',')))
        total_cost = sum(ingredient_costs)

        if total_cost <= budget:
            if total_cost > closest_cost:
                closest_cost = total_cost
                best_recipe = name

    return best_recipe