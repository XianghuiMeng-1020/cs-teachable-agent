def suggest_recipe(budget, recipes):
    best_recipe = 'No recipe available'
    closest_cost = 0
    
    for recipe in recipes:
        name, costs = recipe.split(':')
        total_cost = sum(map(int, costs.split(',')))
        
        if total_cost <= budget and total_cost > closest_cost:
            closest_cost = total_cost
            best_recipe = name
    
    return best_recipe