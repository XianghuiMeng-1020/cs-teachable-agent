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
            print(f'An error occurred while adding the recipe: {e}')

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                content = file.read().strip()  
                recipes = content.split('\n\n')
                for recipe in recipes:
                    lines = recipe.split('\n')
                    if lines[0] == name:
                        return recipe
            return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            return f'An error occurred while retrieving the recipe: {e}'