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
                content = file.read().strip()  
                recipes = content.split('\n\n')
                for recipe in recipes:
                    lines = recipe.split('\n')
                    if lines[0] == name:
                        return lines[1:]  
        except Exception as e:
            print(f'Error retrieving recipe: {e}')  
        return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                contents = file.read()  
                recipes = contents.split('\n\n')
                updated_recipes = [recipe for recipe in recipes if not recipe.startswith(name + '\n')]
                if len(updated_recipes) == len(recipes):
                    return False  

            with open(self.filename, 'w') as file:
                file.write('\n\n'.join(updated_recipes).strip() + '\n')
            return True
        except Exception as e:
            print(f'Error deleting recipe: {e}')  
            return False