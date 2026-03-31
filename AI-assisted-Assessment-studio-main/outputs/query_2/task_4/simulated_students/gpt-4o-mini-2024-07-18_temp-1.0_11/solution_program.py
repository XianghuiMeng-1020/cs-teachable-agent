def organize_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        sections = content.split('/****')
        for section in sections:
            if 'NAME' in section and 'INGREDIENTS' in section:
                name_start = section.find('NAME') + len('NAME\n')
                name_end = section.find('---', name_start)
                recipe_name = section[name_start:name_end].strip()
                recipes.append(recipe_name)
    return sorted(recipes)