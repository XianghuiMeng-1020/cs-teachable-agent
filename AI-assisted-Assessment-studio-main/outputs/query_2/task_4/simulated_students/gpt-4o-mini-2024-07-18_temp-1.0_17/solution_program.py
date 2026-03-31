def organize_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        recipes_blocks = content.split('/****')
        for block in recipes_blocks:
            if 'NAME' in block:
                name_start = block.find('NAME') + len('NAME\n')
                name_end = block.find('\n---', name_start)
                recipe_name = block[name_start:name_end].strip()
                recipes.append(recipe_name)
    return sorted(recipes)