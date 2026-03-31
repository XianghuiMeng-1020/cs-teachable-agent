def organize_recipes(filename):
    recipes = []
    
    with open(filename, 'r') as file:
        content = file.read().strip()
        if not content:
            return []
        
        for recipe_block in content.split('\n\n'):
            lines = recipe_block.strip().split('\n')
            if len(lines) < 2:
                continue

            title = lines[0]
            ingredients = lines[1].split(', ')
            instructions = lines[2:] if len(lines) > 2 else []

            recipes.append({
                'title': title,
                'ingredients': ingredients,
                'instructions': instructions
            })
    
    recipes.sort(key=lambda r: r['title'])
    return recipes