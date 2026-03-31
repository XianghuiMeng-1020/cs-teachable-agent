class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def load_recipes(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if ':' in line:
                        name, ingredients = line.strip().split(':', 1)
                        self.recipes[name] = ingredients.split(',')
        except FileNotFoundError:
            raise Exception('File not found')
        except IOError:
            raise Exception('Error reading file')

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                ingredients_str = ','.join(ingredients)
                file.write(f'{name}:{ingredients_str}\n')
        except IOError:
            raise Exception('Error writing to file')

    def find_recipe(self, name):
        if name not in self.recipes:
            raise ValueError('Recipe not found')
        return self.recipes[name]