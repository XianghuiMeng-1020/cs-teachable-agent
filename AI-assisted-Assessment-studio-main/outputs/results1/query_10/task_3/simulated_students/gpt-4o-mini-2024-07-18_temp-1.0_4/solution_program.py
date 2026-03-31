class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n\n')
        except Exception as e:
            print(f'Error adding recipe: {e}')  # Error handling can be improved

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
                for recipe in recipes:
                    lines = recipe.split('\n')
                    recipe_name = lines[0]
                    if recipe_name == name:
                        return lines[1:]
            return None
        except Exception as e:
            print(f'Error retrieving recipe: {e}') 
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
            updated_recipes = [r for r in recipes if r.split('\n')[0] != name]
            if len(updated_recipes) < len(recipes):
                with open(self.filename, 'w') as file:
                    file.write('\n\n'.join(updated_recipes) + ('\n' if updated_recipes else ''))
                return True
            return False
        except Exception as e:
            print(f'Error deleting recipe: {e}')
            return False