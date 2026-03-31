class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def load_recipes(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    name, ingredients = line.strip().split(':')
                    self.recipes[name] = ingredients.split(',')
        except Exception as e:
            raise e

    def add_recipe(self, name, ingredients, file_path):
        self.recipes[name] = ingredients
        try:
            with open(file_path, 'a') as file:
                file.write(f"{name}:{','.join(ingredients)}\n")
        except Exception as e:
            raise e

    def find_recipe(self, name):
        if name in self.recipes:
            return self.recipes[name]
        else:
            raise ValueError("Recipe not found")