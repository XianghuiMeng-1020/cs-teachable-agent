def suggest_recipe(budget, recipes):
    best_recipe = None
    closest_cost = -1

    for recipe in recipes:
        recipe_name, costs = recipe.split(':')
        total_cost = sum(map(int, costs.split(',')))

        if total_cost <= budget:
            if total_cost > closest_cost:
                closest_cost = total_cost
                best_recipe = recipe_name

    return best_recipe if best_recipe else 'No recipe available'