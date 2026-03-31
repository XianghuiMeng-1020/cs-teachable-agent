def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = []
    recipe_blocks = content.split('/****')
    for block in recipe_blocks:
        if 'NAME' in block and 'INGREDIENTS' in block:
            name_section = block.split('NAME')[1].split('---')[0].strip()
            recipes.append(name_section)

    return sorted(recipes)