class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'An error occurred while adding a recipe: {e}') 

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    if lines[i].strip() == name:
                        recipe = lines[i].strip() + '\n'
                        i += 1
                        while i < len(lines) and lines[i].strip() != '':
                            recipe += lines[i].strip() + '\n'
                            i += 1
                        return recipe.strip() + '\n'
                    i += 1
                return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            print(f'An error occurred while retrieving a recipe: {e}')