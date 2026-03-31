class RecipeManager:
    def __init__(self):
        self.filename = 'recipes.txt'
        self.recipes = []
        try:
            with open(self.filename, 'r') as file:
                self.recipes = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.recipes = []

    def add_recipe(self, recipe_name):
        if recipe_name not in self.recipes:
            self.recipes.append(recipe_name)
            with open(self.filename, 'a') as file:
                file.write(f"{recipe_name}\n")

    def remove_recipe(self, recipe_name):
        if recipe_name in self.recipes:
            self.recipes.remove(recipe_name)
            with open(self.filename, 'w') as file:
                for recipe in self.recipes:
                    file.write(f"{recipe}\n")

    def list_recipes(self):
        return self.recipes