class Recipe:
    def __init__(self, name, ingredients, cooking_method):
        self.name = name
        self.ingredients = ingredients
        self.cooking_method = cooking_method

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
        else:
            raise ValueError('Ingredient not found')

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(f'Recipe: {self.name}\n')
            file.write('Ingredients:\n')
            for ing in self.ingredients:
                file.write(f'- {ing}\n')
            file.write('Cooking Method:\n')
            file.write(f'{self.cooking_method}\n')

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.name = lines[0][8:].strip()
                self.ingredients = []
                ingredient_section = False
                for line in lines[1:]:
                    line = line.strip()
                    if line == 'Ingredients:':
                        ingredient_section = True
                    elif line == 'Cooking Method:':
                        ingredient_section = False
                    elif ingredient_section and line.startswith('- '):
                        self.ingredients.append(line[2:])
                    elif not ingredient_section:
                        self.cooking_method = line
        except FileNotFoundError:
            print('File not found.')