def organize_recipes(filename):
    recipes = []
    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n\n')
        for block in lines:
            parts = block.strip().split('\n')
            title = parts[0]
            ingredients = parts[1].split(', ')
            instructions = parts[2:]
            recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
    return sorted(recipes, key=lambda x: x['title'])