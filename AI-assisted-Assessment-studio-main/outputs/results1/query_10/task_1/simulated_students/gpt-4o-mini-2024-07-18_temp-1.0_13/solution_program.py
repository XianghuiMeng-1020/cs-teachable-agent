class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def load_recipes(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    recipe_name, ingredients = line.strip().split(':')
                    self.recipes[recipe_name] = ingredients.split(',')
        except FileNotFoundError:
            print(f'File not found: {file_path}')
        except IOError:
            print('Error reading file.')

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                file.write(f'{name}:{"",".join(ingredients)}\n')
        except IOError:
            print('Error writing to file.')

    def find_recipe(self, name):
        if name in self.recipes:
            return self.recipes[name]
        else:
            raise ValueError('Recipe not found')