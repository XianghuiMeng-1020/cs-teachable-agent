def organize_recipes(filename):
    recipes = []
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')
        for recipe_block in content:
            lines = recipe_block.strip().split('\n')
            title = lines[0].strip()
            ingredients = lines[1].strip().split(', ')
            instructions = lines[2:]
            recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
    return sorted(recipes, key=lambda x: x['title'])