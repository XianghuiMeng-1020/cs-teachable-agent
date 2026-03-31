def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = []
    sections = content.split('/****')

    for section in sections:
        if 'NAME' in section:
            lines = section.split('\n')
            for line in lines:
                if line.strip().startswith('NAME'):
                    recipe_name = lines[lines.index(line) + 1].strip()
                    recipes.append(recipe_name)
                    break

    return sorted(recipes)