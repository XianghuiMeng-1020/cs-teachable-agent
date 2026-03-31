class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def load_recipes(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    name, ingredients = line.strip().split(':')
                    self.recipes[name] = ingredients.split(',')
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except IOError:
            print(f"Error: Could not read from the file '{file_path}'.")

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                ingredients_line = ','.join(ingredients)
                file.write(f"{name}:{ingredients_line}\n")
        except IOError:
            print(f"Error: Could not write to the file '{file_path}'.")

    def find_recipe(self, name):
        if name in self.recipes:
            return self.recipes[name]
        else:
            raise ValueError("Recipe not found")