def organize_recipes(filename):
    recipes = []
    with open(filename, 'r') as file:
        contents = file.read().strip().split('\n\n')
        for recipe in contents:
            lines = recipe.split('\n')
            title = lines[0].strip()
            ingredients = lines[1].strip().split(', ')
            instructions = [line.strip() for line in lines[2:]]
            recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
    return sorted(recipes, key=lambda x: x['title'])