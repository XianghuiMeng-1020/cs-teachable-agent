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
                content = file.read()
                recipes = content.split('\n\n')
                for recipe in recipes:
                    lines = recipe.strip().split('\n')
                    if lines and lines[0] == name:
                        return lines[1:]
            return None
        except Exception as e:
            print(f'Error retrieving recipe: {e}')  
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
            recipes = content.split('\n\n')
            new_recipes = []
            recipe_found = False
            for recipe in recipes:
                lines = recipe.strip().split('\n')
                if lines and lines[0] == name:
                    recipe_found = True
                    continue
                new_recipes.append(recipe)
            with open(self.filename, 'w') as file:
                file.write('\n\n'.join(new_recipes) + '\n')
            return recipe_found
        except Exception as e:
            print(f'Error deleting recipe: {e}')
            return False