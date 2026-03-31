def suggest_recipe(budget, recipes):
    closest_recipe = "No recipe available"
    closest_cost = -1

    for recipe in recipes:
        name, ingredients = recipe.split(':')
        ingredient_costs = map(int, ingredients.split(','))
        total_cost = sum(ingredient_costs)

        if total_cost <= budget and total_cost > closest_cost:
            closest_cost = total_cost
            closest_recipe = name

    return closest_recipe

# Example test
print(suggest_recipe(10, ["Pasta:5,5", "Salad:3,2,1,4", "Soup:6,3", "Sandwich:5,5"]))