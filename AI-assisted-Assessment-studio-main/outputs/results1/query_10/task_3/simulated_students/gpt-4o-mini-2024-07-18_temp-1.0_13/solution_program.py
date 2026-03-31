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
            print(f'Error adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
                for recipe in recipes:
                    lines = recipe.split('\n')
                    recipe_name = lines[0].strip()
                    if recipe_name == name:
                        return [line.strip() for line in lines[1:] if line.strip()]
            return None
        except Exception as e:
            print(f'Error retrieving recipe: {e}')  
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                recipes = file.read().strip().split('\n\n')
            new_recipes = [recipe for recipe in recipes if not recipe.startswith(name + '\n')]
            if len(new_recipes) < len(recipes):
                with open(self.filename, 'w') as file:
                    file.write('\n\n'.join(new_recipes) + '\n')
                return True
            return False
        except Exception as e:
            print(f'Error deleting recipe: {e}')  
            return False