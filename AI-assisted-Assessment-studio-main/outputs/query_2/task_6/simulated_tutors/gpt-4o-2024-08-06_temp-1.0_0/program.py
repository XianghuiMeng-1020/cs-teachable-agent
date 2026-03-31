def generate_shopping_list(recipes_file, available_file, output_file):
    def parse_ingredients(file_name):
        with open(file_name, 'r') as file:
            content = file.read()
            # Split recipes by empty lines and strip to clean whitespace
            recipes = [recipe.strip() for recipe in content.split('\n\n')]
            # Extract ingredients from each recipe
            ingredients = set()
            for recipe in recipes:
                lines = recipe.split('\n')
                ingredients.update(lines[1:])  # ignore the first line which is the recipe name
            return set(ingredient.lower() for ingredient in ingredients)  # case insensitive comparison

    def parse_available(file_name):
        with open(file_name, 'r') as file:
            # Read available ingredients and strip each one
            return set(line.strip().lower() for line in file if line.strip())  # case insensitive

    # Parse the ingredients from both files
    recipe_ingredients = parse_ingredients(recipes_file)
    available_ingredients = parse_available(available_file)

    # Find missing ingredients
    missing_ingredients = sorted(recipe_ingredients - available_ingredients)

    # Write missing ingredients to the output file
    with open(output_file, 'w') as file:
        for ingredient in missing_ingredients:
            file.write(ingredient + '\n')
