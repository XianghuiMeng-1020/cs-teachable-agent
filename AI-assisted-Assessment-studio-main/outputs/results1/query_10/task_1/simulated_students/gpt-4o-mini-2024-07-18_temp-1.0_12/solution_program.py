class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def load_recipes(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    recipe = line.strip().split(':')
                    if len(recipe) == 2:
                        name = recipe[0].strip()
                        ingredients = recipe[1].strip().split(',')
                        self.recipes[name] = [ingredient.strip() for ingredient in ingredients]
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except IOError:
            print("Error: An I/O error occurred while reading the file.")

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = [ingredient.strip() for ingredient in ingredients.split(',')]
        try:
            with open(file_path, 'a') as file:
                file.write(f"{name}:{','.join(self.recipes[name])}\n")
        except IOError:
            print("Error: An I/O error occurred while writing to the file.")

    def find_recipe(self, name):
        if name in self.recipes:
            return self.recipes[name]
        else:
            raise ValueError("Recipe not found")