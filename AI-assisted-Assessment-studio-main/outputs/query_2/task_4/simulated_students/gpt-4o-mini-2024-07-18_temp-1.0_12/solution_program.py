def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = []
    blocks = content.split('/****')

    for block in blocks:
        if 'NAME' in block:
            name_section = block.split('NAME')[1]
            name = name_section.split('---')[0].strip()
            if name:
                recipes.append(name)

    return sorted(recipes)