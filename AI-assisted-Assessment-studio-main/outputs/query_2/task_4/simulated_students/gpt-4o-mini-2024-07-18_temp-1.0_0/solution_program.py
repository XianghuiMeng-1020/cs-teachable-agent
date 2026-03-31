def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = content.split('/****')
    recipe_names = []

    for recipe in recipes:
        if 'NAME' in recipe:
            sections = recipe.split('---')
            for section in sections:
                if 'NAME' in section:
                    lines = section.strip().split('\n')
                    for line in lines:
                        if line.strip() and line.strip() != 'NAME':
                            recipe_names.append(line.strip())

    return sorted(recipe_names)