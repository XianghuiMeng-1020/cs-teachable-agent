def organize_recipes(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    recipes = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line:
            title = line
            i += 1
            ingredients = lines[i].strip().split(', ')
            i += 1
            instructions = []
            while i < len(lines) and lines[i].strip():
                instructions.append(lines[i].strip())
                i += 1
            recipes.append({
                'title': title,
                'ingredients': ingredients,
                'instructions': instructions
            })
        i += 1
    return sorted(recipes, key=lambda x: x['title'])