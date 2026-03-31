class RecipeManager:
    def __init__(self):
        self.recipes = {}
        self.load_recipes()

    def add_recipe(self, name, ingredients, instructions):
        if name in self.recipes:
            raise Exception('Recipe with this name already exists.')
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

    def load_recipes(self):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.read().strip().split('\n')
                for i in range(0, len(lines), 3):
                    name = lines[i]
                    ingredients = lines[i + 1].split(', ')
                    instructions = lines[i + 2]
                    self.recipes[name] = {'ingredients': ingredients, 'instructions': instructions}
        except FileNotFoundError:
            pass

    def save_recipes(self):
        with open('recipes.txt', 'w') as file:
            for name, details in self.recipes.items():
                file.write(f'{name}\n')
                file.write(', '.join(details['ingredients']) + '\n')
                file.write(details['instructions'] + '\n')