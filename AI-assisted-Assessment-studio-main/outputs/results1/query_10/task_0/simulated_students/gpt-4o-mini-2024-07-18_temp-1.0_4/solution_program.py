class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                for ingredient in ingredients:
                    file.write(ingredient + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'Error while adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
                for recipe in recipes:
                    if recipe.startswith(name + '\n'):
                        return recipe
            return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            return f'Error while retrieving recipe: {e}'