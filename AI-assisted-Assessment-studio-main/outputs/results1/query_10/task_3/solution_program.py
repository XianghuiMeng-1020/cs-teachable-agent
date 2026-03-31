class RecipeManager:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients):
        with open(self.file_name, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write('\n')

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                content = file.read().split("\n\n")
                for recipe in content:
                    lines = recipe.strip().split('\n')
                    if lines[0] == name:
                        return lines[1:]
        except Exception:
            pass
        return None

    def delete_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                recipes = file.read().split("\n\n")
            new_recipes = []
            found = False
            for recipe in recipes:
                if recipe.startswith(name + '\n'):
                    found = True
                else:
                    new_recipes.append(recipe)
            if found:
                with open(self.file_name, 'w') as file:
                    file.write("\n\n".join(new_recipes))
                return True
        except Exception:
            pass
        return False