def find_recipes_with_ingredient(file_path, ingredient):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        # Split recipes by two new lines
        recipe_blocks = content.strip().split('\n\n')
        for block in recipe_blocks:
            lines = block.strip().split('\n')
            recipe_name = lines[0]
            ingredients = lines[1:]
            # Check if ingredient is in the current recipe's ingredients
            if ingredient in ingredients:
                recipes.append(recipe_name)
    return recipes