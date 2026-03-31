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
            print(f'Error adding recipe: {str(e)}')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as f:
                lines = f.read().strip().split('\n\n')
                for block in lines:
                    parts = block.split('\n')
                    recipe_name = parts[0].strip()
                    if recipe_name == name:
                        return [ingredient.strip() for ingredient in parts[1:]]
            return None
        except Exception as e:
            print(f'Error retrieving recipe: {str(e)}')
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as f:
                lines = f.read().strip().split('\n\n')
            new_lines = [block for block in lines if not block.startswith(name + '\n')]
            if len(new_lines) == len(lines):
                return False
            with open(self.filename, 'w') as f:
                f.write('\n\n'.join(new_lines) + ('\n' if new_lines else ''))
            return True
        except Exception as e:
            print(f'Error deleting recipe: {str(e)}')
            return False