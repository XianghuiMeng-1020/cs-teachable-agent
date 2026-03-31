def can_cook_recipe(recipe, ingredients_file):
    # Initialize an empty dictionary to store ingredient quantities
    available = {}
    
    # Read from the ingredients file
    with open(ingredients_file, 'r') as file:
        for line in file:
            # Clean and split the line to extract ingredient name and quantity
            ingredient, quantity = line.strip().split(',')
            available[ingredient] = int(quantity)
    
    # Check each ingredient in the recipe
    for item, needed in recipe.items():
        # If the ingredient is not available or not enough quantity, return False
        if item not in available or available[item] < needed:
            return False
    
    # All ingredients are available in required quantities
    return True