class RecipeManager:
    def add_recipe(self, name, ingredients, steps):
        try:
            with open('recipes.txt', 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'An error occurred while adding the recipe: {e}')

    def get_recipe(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                recipes = file.read().strip().split('\n\n')
                for recipe in recipes:
                    if recipe.startswith(name + '\n'):
                        return recipe
                return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            return f'An error occurred while retrieving the recipe: {e}'