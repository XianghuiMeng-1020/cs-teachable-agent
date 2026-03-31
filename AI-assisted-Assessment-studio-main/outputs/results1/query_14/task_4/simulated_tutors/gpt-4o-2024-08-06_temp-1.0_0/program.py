def ingredient_quantifier(recipe):
    if not recipe:
        return "The recipe requires no ingredients."
    
    # Create list to store formatted ingredient parts
    ingredient_list = []
    for ingredient, quantity in recipe.items():
        # Concatenate the quantity and ingredient
        ingredient_list.append(f"{quantity} of {ingredient}")
        
    # Join the list into a single string with appropriate format
    return "To make this recipe, you will need: " + ", ".join(ingredient_list)