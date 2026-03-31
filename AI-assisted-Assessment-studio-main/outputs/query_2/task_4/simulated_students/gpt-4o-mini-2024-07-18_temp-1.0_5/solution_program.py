def organize_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        blocks = content.split('/****')
        for block in blocks:
            if 'NAME' in block:
                # Extract recipe name
                sections = block.split('---')
                for section in sections:
                    if 'NAME' in section:
                        # Find the name, it's the first line after 'NAME'
                        name_line = section.split('\n')
                        if len(name_line) > 1:
                            recipe_name = name_line[1].strip()
                            if recipe_name:
                                recipes.append(recipe_name)

    return sorted(recipes)