def organize_recipes(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')

    recipes = []
    for entry in content:
        lines = entry.split('\n')
        title = lines[0].strip()
        ingredients = lines[1].split(', ')
        instructions = lines[2:]
        recipes.append({
            'title': title,
            'ingredients': [ingredient.strip() for ingredient in ingredients],
            'instructions': [instruction.strip() for instruction in instructions]
        })

    return sorted(recipes, key=lambda x: x['title'])