def organize_recipes(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')

    recipes = []
    for recipe in content:
        lines = recipe.split('\n')
        title = lines[0].strip()
        ingredients = [i.strip() for i in lines[1].split(',')]
        instructions = [line.strip() for line in lines[2:]]
        recipes.append({
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions
        })

    return sorted(recipes, key=lambda x: x['title'])