class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients):
        try:
            with open(self.filename, 'a') as f:
                f.write(name + '\n')
                for ingredient in ingredients:
                    f.write(ingredient + '\n')
                f.write('\n')
        except Exception as e:
            print(f'Error adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as f:
                recipes = f.read().strip().split('\n\n')
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
            with open(self.filename, 'r') as f:
                recipes = f.read().strip().split('\n\n')
            updated_recipes = [recipe for recipe in recipes if recipe.split('\n')[0] != name]
            if len(updated_recipes) == len(recipes):
                return False
            with open(self.filename, 'w') as f:
                f.write('\n\n'.join(updated_recipes) + ('\n' if updated_recipes else ''))
            return True
        except Exception as e:
            print(f'Error deleting recipe: {e}')
            return False
