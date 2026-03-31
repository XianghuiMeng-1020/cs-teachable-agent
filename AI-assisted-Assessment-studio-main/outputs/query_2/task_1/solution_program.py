def find_recipes_with_ingredient(file_path, ingredient):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    current_recipe = None
    recipes = []
    results = []

    for line in lines:
        line = line.strip()
        if line:  
            if not current_recipe:  
                current_recipe = line
                recipes.append((current_recipe, []))
            else:  
                recipes[-1][1].append(line)  
        else:  
            current_recipe = None

    for recipe, ingredients in recipes:
        if ingredient in ingredients:
            results.append(recipe)

    return results
