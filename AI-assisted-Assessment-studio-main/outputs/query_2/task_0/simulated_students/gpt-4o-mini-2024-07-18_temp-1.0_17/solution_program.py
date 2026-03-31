def organize_recipes(filename):
    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n\n')

    recipes = []
    for recipe in lines:
        parts = recipe.strip().split('\n')
        title = parts[0].strip()
        ingredients = parts[1].strip().split(', ')
        instructions = parts[2:]
        recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})

    return sorted(recipes, key=lambda r: r['title'])