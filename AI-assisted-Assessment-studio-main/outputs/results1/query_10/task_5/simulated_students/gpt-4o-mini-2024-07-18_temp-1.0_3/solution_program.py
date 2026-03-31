class Recipe:
    def __init__(self, name, ingredients=None, cooking_method=''):
        self.name = name
        self.ingredients = ingredients if ingredients is not None else []
        self.cooking_method = cooking_method

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient):
        try:
            self.ingredients.remove(ingredient)
        except ValueError:
            raise ValueError('Ingredient not found')

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(f'Recipe: {self.name}\n')
            file.write('Ingredients:\n')
            for ingredient in self.ingredients:
                file.write(f'- {ingredient}\n')
            file.write('Cooking Method:\n')
            file.write(f'{self.cooking_method}')

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip().split(': ')[1]
                self.ingredients = []
                ingredient_lines = lines[2:-1]
                for line in ingredient_lines:
                    self.ingredients.append(line.strip()[2:])  # Skip the '- '
                self.cooking_method = lines[-1].strip().split(': ')[1]
        except FileNotFoundError:
            print('File not found')
        except Exception as e:
            print(f'An error occurred: {e)'}