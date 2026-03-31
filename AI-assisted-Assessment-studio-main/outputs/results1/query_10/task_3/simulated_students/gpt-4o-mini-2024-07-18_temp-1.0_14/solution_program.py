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
                content = f.read().strip().split('\n\n')
                for recipe in content:
                    if recipe.startswith(name + '\n'):
                        return recipe.split('\n')[1:]
        except Exception as e:
            print(f'Error retrieving recipe: {e}')
        return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as f:
                content = f.read().strip().split('\n\n')
            new_content = []
            found = False
            for recipe in content:
                if recipe.startswith(name + '\n'):
                    found = True
                else:
                    new_content.append(recipe)
            with open(self.filename, 'w') as f:
                f.write('\n\n'.join(new_content) + ('\n' if new_content else ''))
            return found
        except Exception as e:
            print(f'Error deleting recipe: {e}')
        return False