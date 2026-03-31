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
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                file.write(f"{name}:{','.join(ingredients)}\n")
        except Exception as e:
            print(f"An error occurred while saving the recipe: {e}")

    def find_recipe(self, name):
        if name not in self.recipes:
            raise ValueError("Recipe not found")
        return self.recipes[name]