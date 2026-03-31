def calculate_ingredients(recipes):
    # A dictionary to store the total quantities of each ingredient.
    total_ingredients = {}
    
    # Iterate over each recipe in the list.
    for recipe in recipes:
        # Split each recipe into its respective quantity:ingredient pairs.
        items = recipe.split()
        for item in items:
            try:
                # Split the quantity from the ingredient.
                quantity, ingredient = item.split(':')
                quantity = int(quantity)  # Convert the quantity to integer.
                
                # Add the quantity to the total for the ingredient in the dictionary.
                if ingredient in total_ingredients:
                    total_ingredients[ingredient] += quantity
                else:
                    total_ingredients[ingredient] = quantity
            except ValueError:
                print(f"Error processing item: {item}")
                continue  # In case there's a problem, skip to the next item.
    
    return total_ingredients
    
# Example usage of the function.
print(calculate_ingredients(["2:egg 3:flour 1:sugar", "1:egg 2:sugar 1:flour"]))