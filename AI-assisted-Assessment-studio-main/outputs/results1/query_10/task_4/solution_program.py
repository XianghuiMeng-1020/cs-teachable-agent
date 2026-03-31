class RecipeManager:
    def __init__(self):
        self.recipes = []
        try:
            with open('recipes.txt', 'r') as file:
                self.recipes = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def add_recipe(self, recipe_name):
        if recipe_name not in self.recipes:
            self.recipes.append(recipe_name)
            with open('recipes.txt', 'a') as file:
                file.write(recipe_name + '\n')

    def remove_recipe(self, recipe_name):
        if recipe_name in self.recipes:
            self.recipes.remove(recipe_name)
            with open('recipes.txt', 'w') as file:
                for recipe in self.recipes:
                    file.write(recipe + '\n')

    def list_recipes(self):
        return self.recipes