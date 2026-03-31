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
            print(f'Error while adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                content = file.read().strip().split('\n\n')
                for recipe in content:
                    lines = recipe.strip().split('\n')
                    if lines[0] == name:
                        return lines[1:]
        except Exception as e:
            print(f'Error while retrieving recipe: {e}')  
        return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                content = file.read().strip().split('\n\n')
            updated_content = [recipe for recipe in content if not recipe.startswith(name + '\n')]
            if len(updated_content) == len(content):
                return False
            with open(self.filename, 'w') as file:
                file.write('\n\n'.join(updated_content) + ('\n' if updated_content else ''))
            return True
        except Exception as e:
            print(f'Error while deleting recipe: {e}')  
        return False