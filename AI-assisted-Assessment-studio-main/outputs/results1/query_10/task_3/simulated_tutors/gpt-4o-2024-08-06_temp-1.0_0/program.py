class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients):
        try:
            with open(self.filename, 'a') as f:
                f.write(f"{name}\n")
                for ingredient in ingredients:
                    f.write(f"{ingredient}\n")
                f.write("\n")
        except IOError as e:
            print(f"An error occurred: {e}")

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as f:
                lines = f.read().strip().split('\n\n')
                for recipe in lines:
                    recipe_lines = recipe.split('\n')
                    if recipe_lines[0] == name:
                        return recipe_lines[1:]
        except IOError as e:
            print(f"An error occurred: {e}")
            return None
        return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as f:
                lines = f.read().strip().split('\n\n')
            with open(self.filename, 'w') as f:
                deleted = False
                for recipe in lines:
                    if recipe.split('\n')[0] == name:
                        deleted = True
                    else:
                        f.write(recipe + '\n\n')
                return deleted
        except IOError as e:
            print(f"An error occurred: {e}")
            return False