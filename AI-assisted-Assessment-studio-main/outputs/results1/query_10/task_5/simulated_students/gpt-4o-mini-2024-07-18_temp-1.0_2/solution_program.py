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
        try:
            with open(filename, 'w') as file:
                file.write(f'Recipe: {self.name}\n')
                file.write('Ingredients:\n')
                for ing in self.ingredients:
                    file.write(f'- {ing}\n')
                file.write('Cooking Method:\n')
                file.write(f'{self.cooking_method}\n')
        except Exception as e:
            print(f'An error occurred while saving to file: {e}') 

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip().split(': ')[1]
                self.ingredients = []
                ing_section = True
                for line in lines[1:]:
                    if line.strip() == 'Ingredients:':
                        continue
                    elif line.strip() == 'Cooking Method:':
                        ing_section = False
                        continue
                    if ing_section:
                        self.ingredients.append(line.strip().lstrip('- '))
                    else:
                        self.cooking_method = line.strip()
        except FileNotFoundError:
            print('The file does not exist.')
        except Exception as e:
            print(f'An error occurred while loading from file: {e)'}