class Recipe:
    def __init__(self, name, ingredients, cooking_method):
        self.name = name
        self.ingredients = ingredients if ingredients else []
        self.cooking_method = cooking_method

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient):
        try:
            self.ingredients.remove(ingredient)
        except ValueError:
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
            raise e

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].split(': ')[1].strip()
                self.ingredients = []
                i = 2  # Start reading ingredients after the "Ingredients:" line
                while lines[i].strip().startswith('-'):
                    self.ingredients.append(lines[i].strip()[2:])  # Skip "- "
                    i += 1
                self.cooking_method = lines[i+1].strip()
        except FileNotFoundError:
            raise FileNotFoundError("The specified file does not exist.")
        except Exception as e:
            raise e