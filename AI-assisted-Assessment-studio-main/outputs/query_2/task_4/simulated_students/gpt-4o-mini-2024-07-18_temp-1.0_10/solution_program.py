def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    recipes = content.split('/****')
    recipe_names = []
    for recipe in recipes:
        if 'NAME' in recipe:
            parts = recipe.split('---')
            for part in parts:
                if 'NAME' in part:
                    name = part.split('\n')[-2].strip()
                    recipe_names.append(name)
    return sorted(recipe_names)