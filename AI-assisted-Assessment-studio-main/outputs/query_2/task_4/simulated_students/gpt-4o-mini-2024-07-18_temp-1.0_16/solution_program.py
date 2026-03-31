def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = content.strip().split("\n\n")
    recipe_names = []

    for recipe in recipes:
        lines = recipe.split("\n")
        if len(lines) >= 3:
            name_line = lines[1].strip()
            recipe_names.append(name_line)

    return sorted(recipe_names)