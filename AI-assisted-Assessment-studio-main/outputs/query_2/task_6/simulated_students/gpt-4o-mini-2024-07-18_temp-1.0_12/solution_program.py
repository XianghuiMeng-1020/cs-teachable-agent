def generate_shopping_list(recipes_file, available_file, output_file):
    with open(recipes_file, 'r') as rf:
        recipes_content = rf.read()
    
    recipes = recipes_content.split('\n\n')
    missing_ingredients = set()
    
    for recipe in recipes:
        lines = recipe.strip().split('\n')
        if not lines:
            continue
        for ingredient in lines[1:]:
            missing_ingredients.add(ingredient.strip().lower())
    
    with open(available_file, 'r') as af:
        available_content = af.read()
        available_ingredients = {line.strip().lower() for line in available_content.splitlines()} 
    
    shopping_list = sorted(missing_ingredients - available_ingredients)
    
    with open(output_file, 'w') as of:
        for ingredient in shopping_list:
            of.write(ingredient + '\n')