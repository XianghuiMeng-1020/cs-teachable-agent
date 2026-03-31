class RecipeManager:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.file_name, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'Error while adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                recipes = file.read().strip().split('\n\n')
                for recipe in recipes:
                    lines = recipe.split('\n')
                    if lines[0] == name:
                        return {'name': lines[0], 'ingredients': lines[1:-1], 'steps': lines[-1]}
                return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe file not found'
        except Exception as e:
            return f'Error while retrieving recipe: {e}'