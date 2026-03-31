class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n\n')
        except Exception as e:
            print(f'Error adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
                for recipe in recipes:
                    lines = recipe.strip().split('\n')
                    if lines[0] == name:
                        return lines[1:]
        except Exception as e:
            print(f'Error getting recipe: {e}')  
        return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
            updated_recipes = [recipe for recipe in recipes if not recipe.startswith(name + '\n')]
            if len(updated_recipes) < len(recipes):
                with open(self.filename, 'w') as file:
                    file.write('\n\n'.join(updated_recipes) + '\n')
                return True
        except Exception as e:
            print(f'Error deleting recipe: {e}')  
        return False