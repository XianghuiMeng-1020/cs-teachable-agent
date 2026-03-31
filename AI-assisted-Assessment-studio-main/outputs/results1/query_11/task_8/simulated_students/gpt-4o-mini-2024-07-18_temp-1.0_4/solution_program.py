def suggest_recipe(budget, recipes):
    closest_recipe = None
    closest_cost = -1

    for recipe in recipes:
        name, costs_string = recipe.split(':')
        costs = list(map(int, costs_string.split(',')))
        total_cost = sum(costs)

        if total_cost <= budget and total_cost > closest_cost:
            closest_cost = total_cost
            closest_recipe = name

    return closest_recipe if closest_recipe is not None else 'No recipe available'