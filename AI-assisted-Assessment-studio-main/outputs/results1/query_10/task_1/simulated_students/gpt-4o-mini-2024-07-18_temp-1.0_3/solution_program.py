class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def load_recipes(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if ':' in line:
                        recipe_name, ingredients = line.strip().split(':', 1)
                        self.recipes[recipe_name] = ingredients.split(',')
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except IOError:
            print("Error: An error occurred while reading the file.")

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                ingredients_str = ','.join(ingredients)
                file.write(f"{name}:{ingredients_str}\n")
        except IOError:
            print("Error: An error occurred while writing to the file.")

    def find_recipe(self, name):
        if name in self.recipes:
            return self.recipes[name]
        else:
            raise ValueError("Recipe not found")