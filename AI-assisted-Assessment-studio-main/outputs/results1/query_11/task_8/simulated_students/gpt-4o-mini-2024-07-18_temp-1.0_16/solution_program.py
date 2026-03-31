def suggest_recipe(budget, recipes):
    best_cost = -1
    best_recipe = 'No recipe available'

    for recipe in recipes:
        name, costs = recipe.split(':')
        total_cost = sum(map(int, costs.split(',')))

        if total_cost <= budget and total_cost > best_cost:
            best_cost = total_cost
            best_recipe = name

    return best_recipe