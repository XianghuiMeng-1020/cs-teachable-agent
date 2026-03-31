import os

class RecipeManager:
    def __init__(self):
        self.recipes_file = 'recipes.txt'
        self.recipes = self.load_recipes()

    def load_recipes(self):
        if not os.path.exists(self.recipes_file):
            return {}
        recipes = {}
        with open(self.recipes_file, 'r') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                name = lines[i].strip()
                i += 1
                ingredients = lines[i].strip().split(', ')
                i += 1
                instructions = lines[i].strip()
                recipes[name] = {'ingredients': ingredients, 'instructions': instructions}
                i += 1
        return recipes

    def save_recipes(self):
        with open(self.recipes_file, 'w') as file:
            for name, details in self.recipes.items():
                file.write(f'{name}\n')
                file.write(', '.join(details['ingredients']) + '\n')
                file.write(f'{details['instructions']}\n')

    def add_recipe(self, name, ingredients, instructions):
        if name in self.recipes:
            raise Exception('Recipe with this name already exists')
        self.recipes[name] = {'ingredients': ingredients, 'instructions': instructions}
        self.save_recipes()

    def get_recipe(self, name):
        return self.recipes.get(name, None)

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()
            return True
        return False