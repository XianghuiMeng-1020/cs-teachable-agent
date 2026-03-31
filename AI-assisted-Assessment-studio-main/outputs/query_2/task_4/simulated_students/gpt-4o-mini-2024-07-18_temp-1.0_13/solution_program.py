def organize_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        blocks = content.split('/****')
        for block in blocks[1:]:
            name_line = block.split('---')[0].strip().split('\n')[1].strip()
            recipes.append(name_line)
    return sorted(recipes)