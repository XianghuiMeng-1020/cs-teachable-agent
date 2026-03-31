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
            print(f'An error occurred while adding the recipe: {e}')

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
            print(f'An error occurred while retrieving the recipe: {e}')
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
            new_recipes = [recipe for recipe in recipes if recipe.split('\n')[0] != name]
            if len(recipes) == len(new_recipes):
                return False
            with open(self.filename, 'w') as file:
                for recipe in new_recipes:
                    file.write(recipe + '\n\n')
            return True
        except Exception as e:
            print(f'An error occurred while deleting the recipe: {e}')
            return False