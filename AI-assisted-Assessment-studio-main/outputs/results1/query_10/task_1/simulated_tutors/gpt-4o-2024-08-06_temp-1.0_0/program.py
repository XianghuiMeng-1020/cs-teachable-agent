class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def load_recipes(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    name, ingredients_str = line.strip().split(':')
                    ingredients = ingredients_str.split(',')
                    self.recipes[name] = ingredients
        except OSError as e:
            raise OSError("An error occurred while trying to read the file.") from e

    def add_recipe(self, name, ingredients, file_path):
        if name in self.recipes:
            raise ValueError("Recipe already exists.")
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                file.write(f"{name}:{','.join(ingredients)}\n")
        except OSError as e:
            raise OSError("An error occurred while trying to write to the file.") from e

    def find_recipe(self, name):
        if name not in self.recipes:
            raise ValueError("Recipe not found")
        return self.recipes[name]

# This implementation defines a RecipeBook class with functions to work with recipes stored in a file.