def recipe_ingredients_calculator(file_path):
    # Read the file and get all lines
    with open(file_path, 'r') as file:
        recipes = file.readlines()
    
    ingredients_set = set()
    
    # Process each line to extract ingredients
    for recipe in recipes:
        # Split the recipe name from the ingredients
        name, ingredients = recipe.split(':')
        
        # Split the ingredients by comma and add them to the set
        ingredients_list = ingredients.strip().split(',')
        for ingredient in ingredients_list:
            ingredients_set.add(ingredient.strip())
    
    # Convert the set to a sorted list
    sorted_ingredients = sorted(ingredients_set)
    
    return sorted_ingredients