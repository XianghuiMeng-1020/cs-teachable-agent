def ingredient_substitutes(recipe, substitutes):
    # Create a new dictionary to store the result
    substituted_recipe = {}
    
    # Iterate over each ingredient in the recipe
    for ingredient, quantity in recipe.items():
        # Check if there is a substitute for this ingredient
        if ingredient in substitutes:
            # If there is a substitute, use it
            substitute_ingredient = substitutes[ingredient]
        else:
            # If there is no substitute, keep the original ingredient
            substitute_ingredient = ingredient
        
        # Add the ingredient and its quantity to the substituted recipe
        substituted_recipe[substitute_ingredient] = quantity
        
    return substituted_recipe