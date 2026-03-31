def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = content.split('/****')
    recipe_names = []

    for recipe in recipes:
        if 'NAME' in recipe and '---' in recipe:
            name_start = recipe.find('NAME') + len('NAME')
            name_end = recipe.find('---', name_start)
            name = recipe[name_start:name_end].strip()
            if name:
                recipe_names.append(name)

    recipe_names.sort()
    return recipe_names
