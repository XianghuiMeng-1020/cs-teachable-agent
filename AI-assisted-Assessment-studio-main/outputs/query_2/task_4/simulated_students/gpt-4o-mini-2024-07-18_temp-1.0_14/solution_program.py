def organize_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        recipe_blocks = content.split('\\/\*\*\*\*')
        for block in recipe_blocks:
            if 'NAME' in block:
                lines = block.split('\n')
                name_line = next((line for line in lines if 'NAME' in line), None)
                if name_line:
                    name_index = lines.index(name_line) + 1
                    recipe_name = lines[name_index].strip()
                    recipes.append(recipe_name)
    return sorted(recipes)