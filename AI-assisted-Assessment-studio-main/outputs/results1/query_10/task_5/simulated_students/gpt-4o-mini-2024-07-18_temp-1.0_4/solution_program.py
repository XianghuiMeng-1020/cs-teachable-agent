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
            raise ValueError("Ingredient not found")

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                file.write(f'Recipe: {self.name}\n')
                file.write('Ingredients:\n')
                for ingredient in self.ingredients:
                    file.write(f'- {ingredient}\n')
                file.write(f'Cooking Method:\n')
                file.write(f'{self.cooking_method}\n')
        except Exception as e:
            print(f'An error occurred while saving to file: {e}')  

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip().split(': ')[1]
                self.ingredients.clear()
                ingredient_section = False
                for line in lines[1:]:
                    if line.startswith('Ingredients:'):
                        ingredient_section = True
                        continue
                    if ingredient_section:
                        if line.startswith('- '):
                            self.ingredients.append(line.strip()[2:])
                        elif line.startswith('Cooking Method:'):
                            ingredient_section = False
                            self.cooking_method = line.strip().split(': ')[1]
        except FileNotFoundError:
            print('The file does not exist.')
        except Exception as e:
            print(f'An error occurred while loading from file: {e}')