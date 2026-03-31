import os

class RecipeManager:
    def __init__(self):
        self.recipes = []
        self.load_recipes()

    def load_recipes(self):
        try:
            with open('recipes.txt', 'r') as file:
                self.recipes = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.recipes = []
        except Exception as e:
            print(f"An error occurred while loading recipes: {e}")

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
            print(f"An error occurred while saving recipes: {e}")

    def list_recipes(self):
        return self.recipes