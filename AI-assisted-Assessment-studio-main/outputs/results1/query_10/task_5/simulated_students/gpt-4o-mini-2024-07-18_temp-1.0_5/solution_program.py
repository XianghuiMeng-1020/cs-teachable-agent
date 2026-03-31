class Recipe:
    def __init__(self, name, ingredients, cooking_method):
        self.name = name
        self.ingredients = ingredients
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
            file.write(f'{self.cooking_method}\n')

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip().split(': ')[1]
                self.ingredients = []
                i = 2
                while lines[i].startswith('-'):
                    self.ingredients.append(lines[i][2:].strip())
                    i += 1
                self.cooking_method = lines[i+1].strip()
        except FileNotFoundError:
            print('File not found')
        except Exception as e:
            print('An error occurred:', e)