def organize_recipes(filename):
    recipes = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            title = lines[i].strip()
            ingredients = lines[i + 1].strip().split(', ')
            instructions = []
            i += 2
            while i < len(lines) and lines[i].strip() != '':
                instructions.append(lines[i].strip())
                i += 1
            recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
            i += 1
    return sorted(recipes, key=lambda x: x['title'])