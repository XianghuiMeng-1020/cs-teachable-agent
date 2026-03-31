class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                for ingredient in ingredients:
                    file.write(ingredient + '\n')
                file.write('\n')
        except Exception as e:
            print(f'Error adding recipe: {e}')  # Handle exception gracefully

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                current_recipe = None
                recipe_ingredients = []
                for line in lines:
                    line = line.strip()
                    if line == '':  # Blank line indicates a new recipe
                        if current_recipe == name:
                            return recipe_ingredients
                        current_recipe = None
                        recipe_ingredients = []
                    else:
                        if current_recipe is None:
                            current_recipe = line
                        elif current_recipe == name:
                            recipe_ingredients.append(line)
                return recipe_ingredients if current_recipe == name else None
        except Exception as e:
            print(f'Error retrieving recipe: {e}')  # Handle exception gracefully
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()

            recipe_found = False
            new_lines = []
            current_recipe = None
            for line in lines:
                line = line.strip()
                if line == '':  # Blank line indicates a new recipe
                    if current_recipe == name:
                        recipe_found = True
                        current_recipe = None
                    else:
                        new_lines.append('\n')  # Maintain blank line for other recipes
                else:
                    if current_recipe is None:
                        current_recipe = line
                    if current_recipe != name:
                        new_lines.append(line + '\n')  # Keep this recipe

            if recipe_found:
                with open(self.filename, 'w') as file:
                    file.writelines(new_lines)
                return True
            return False
        except Exception as e:
            print(f'Error deleting recipe: {e}')  # Handle exception gracefully
            return False