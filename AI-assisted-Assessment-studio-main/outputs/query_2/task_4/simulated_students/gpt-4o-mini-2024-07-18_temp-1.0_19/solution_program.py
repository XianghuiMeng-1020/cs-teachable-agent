def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = []
    # Split the content using the block comment pattern
    sections = content.split('/****')
    for section in sections:
        if 'NAME' in section:
            # Find the recipe name
            lines = section.split('\n')
            for line in lines:
                if line.strip().startswith('NAME'):
                    name_index = lines.index(line) + 1
                    recipe_name = lines[name_index].strip()
                    recipes.append(recipe_name)

    # Sort the recipe names alphabetically
    sorted_recipes = sorted(recipes)
    return sorted_recipes