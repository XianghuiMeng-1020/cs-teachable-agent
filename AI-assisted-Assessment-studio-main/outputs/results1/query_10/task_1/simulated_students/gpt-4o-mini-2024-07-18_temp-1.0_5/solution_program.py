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
            raise FileNotFoundError("The specified recipe file does not exist.")
        except IOError:
            raise IOError("An error occurred while reading the recipe file.")

    def add_recipe(self, name, ingredients, file_path):
        if name in self.recipes:
            raise ValueError("Recipe already exists.")
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                file.write(f"{name}:{','.join(ingredients)}\n")
        except IOError:
            raise IOError("An error occurred while writing to the recipe file.")

    def find_recipe(self, name):
        if name not in self.recipes:
            raise ValueError("Recipe not found.")
        return self.recipes[name]