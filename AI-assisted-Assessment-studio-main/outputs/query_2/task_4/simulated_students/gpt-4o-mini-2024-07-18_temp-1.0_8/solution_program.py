def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = []

    blocks = content.split('/****')
    for block in blocks[1:]:
        if 'NAME' in block:
            name_section = block.split('---')
            name_line = name_section[0].strip().split('\n')
            for line in name_line:
                if line.startswith('NAME'):
                    continue
                if line.strip():
                    recipes.append(line.strip())

    return sorted(recipes)