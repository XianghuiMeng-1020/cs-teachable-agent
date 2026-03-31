def organize_recipes(filename):
    recipes = []
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')
        for recipe in content:
            lines = recipe.split('\n')
            title = lines[0].strip()
            ingredients = lines[1].split(',')
            instructions = [line.strip() for line in lines[2:]]
            recipes.append({'title': title, 'ingredients': [ingredient.strip() for ingredient in ingredients], 'instructions': instructions})
    return sorted(recipes, key=lambda r: r['title'])