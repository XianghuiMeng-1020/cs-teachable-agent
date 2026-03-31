def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read().strip().split('\n\n')
        recipes = []

        for recipe in content:
            lines = recipe.strip().split('\n')
            if lines:
                recipe_name = lines[0]
                ingredients = lines[1:]
                recipes.append((recipe_name, ingredients))

        recipes.sort(key=lambda x: x[0])

        with open(output_file, 'w') as outfile:
            for i, (name, ingredients) in enumerate(recipes):
                outfile.write(name + '\n')
                for ingredient in ingredients:
                    outfile.write(ingredient + '\n')
                if i < len(recipes) - 1:
                    outfile.write('\n')