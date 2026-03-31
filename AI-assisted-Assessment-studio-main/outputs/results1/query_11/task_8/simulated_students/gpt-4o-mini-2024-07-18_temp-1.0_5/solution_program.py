def suggest_recipe(budget, recipes):
    closest_recipe = None
    closest_cost = -1

    for recipe in recipes:
        name, costs = recipe.split(':')
        total_cost = sum(map(int, costs.split(',')))

        if total_cost <= budget and total_cost > closest_cost:
            closest_recipe = name
            closest_cost = total_cost

    return closest_recipe if closest_recipe else 'No recipe available'