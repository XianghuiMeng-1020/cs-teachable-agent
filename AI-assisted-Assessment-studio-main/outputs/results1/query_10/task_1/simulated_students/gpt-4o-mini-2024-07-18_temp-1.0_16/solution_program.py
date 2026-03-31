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
            print("File not found. Starting with an empty recipe book.")
        except Exception as e:
            print(f'An error occurred while reading the file: {e}')

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                file.write(f'{name}:{','.join(ingredients)}\n')
        except Exception as e:
            print(f'An error occurred while writing to the file: {e}')

    def find_recipe(self, name):
        if name in self.recipes:
            return self.recipes[name]
        else:
            raise ValueError("Recipe not found")