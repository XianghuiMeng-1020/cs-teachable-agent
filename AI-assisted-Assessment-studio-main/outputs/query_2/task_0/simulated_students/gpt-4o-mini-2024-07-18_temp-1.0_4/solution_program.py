def organize_recipes(filename):
    recipes = []
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')
        for entry in content:
            lines = entry.split('\n')
            title = lines[0]
            ingredients = lines[1].split(', ')
            instructions = lines[2:]
            recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
    return sorted(recipes, key=lambda x: x['title'])
