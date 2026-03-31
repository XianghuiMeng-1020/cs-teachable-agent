class RecipeManager:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.file_name, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'Error while adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                current_name = None
                recipe = ''
                for line in lines:
                    line = line.strip()
                    if line == '':
                        if current_name is not None:
                            if current_name == name:
                                return recipe.strip()
                            current_name = None
                            recipe = ''
                    else:
                        if current_name is None:
                            current_name = line
                        else:
                            recipe += line + '\n'
            return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            print(f'Error while retrieving recipe: {e}')