def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    # Split the content by delimiting with the recipe blocks
    recipes_blocks = data.split('/****')

    recipe_names = []

    for block in recipes_blocks:
        if 'NAME' in block:
            # Find the POSITION of NAME section
            name_index_start = block.find('NAME') + len('NAME')
            name_index_end = block.find('---', name_index_start)

            # Extract and clean the NAME
            recipe_name = block[name_index_start:name_index_end].strip()
            if recipe_name:
                recipe_names.append(recipe_name)

    # Sort the names alphabetically
    recipe_names.sort()
    
    return recipe_names
