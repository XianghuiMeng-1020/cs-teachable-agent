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
                file.write('Cooking Method:\n')
                file.write(f'{self.cooking_method}\n')
        except Exception as e:
            print(f'An error occurred while saving the recipe: {e}')  

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip().split(': ')[1]
                self.ingredients = []
                index = 2
                while index < len(lines) and lines[index].startswith('-'):
                    self.ingredients.append(lines[index].strip()[2:])
                    index += 1
                self.cooking_method = lines[-1].strip().split(': ')[1] 
        except FileNotFoundError:
            print('File not found.')
        except Exception as e:
            print(f'An error occurred while loading the recipe: {e}')