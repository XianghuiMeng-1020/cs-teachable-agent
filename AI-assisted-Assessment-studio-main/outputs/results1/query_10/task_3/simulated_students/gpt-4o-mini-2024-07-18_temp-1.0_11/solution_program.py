class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                for ingredient in ingredients:
                    file.write(ingredient + '\n')
                file.write('\n')  # Add a blank line after the recipe
        except Exception as e:
            print(f'Error adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
                for recipe in recipes:
                    lines = recipe.strip().split('\n')
                    if lines[0] == name:
                        return lines[1:]  # Return the list of ingredients
            return None
        except Exception as e:
            print(f'Error retrieving recipe: {e}')  
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
            with open(self.filename, 'w') as file:
                found = False
                for recipe in recipes:
                    lines = recipe.strip().split('\n')
                    if lines[0] != name:
                        file.write(recipe + '\n\n')
                    else:
                        found = True
                return found
        except Exception as e:
            print(f'Error deleting recipe: {e}')
            return False