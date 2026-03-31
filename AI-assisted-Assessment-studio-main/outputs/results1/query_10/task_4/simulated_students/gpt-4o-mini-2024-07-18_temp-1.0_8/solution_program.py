import os

class RecipeManager:
    def __init__(self):
        self.recipes = []
        self.load_recipes()

    def load_recipes(self):
        try:
            if os.path.exists('recipes.txt'):
                with open('recipes.txt', 'r') as file:
                    self.recipes = [line.strip() for line in file.readlines()]
        except Exception as e:
            pass  # Handle exceptions while loading

    def add_recipe(self, recipe_name):
        if recipe_name not in self.recipes:
            self.recipes.append(recipe_name)
            self.save_recipes()

    def remove_recipe(self, recipe_name):
        if recipe_name in self.recipes:
            self.recipes.remove(recipe_name)
            self.save_recipes()

    def save_recipes(self):
        try:
            with open('recipes.txt', 'w') as file:
                for recipe in self.recipes:
                    file.write(recipe + '\n')
        except Exception as e:
            pass  # Handle exceptions while saving

    def list_recipes(self):
        return self.recipes.