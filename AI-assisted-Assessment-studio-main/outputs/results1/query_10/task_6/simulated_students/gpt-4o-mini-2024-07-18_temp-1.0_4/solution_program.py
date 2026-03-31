class RecipeManager:
    def __init__(self):
        self.recipes = {}
        self.load_recipes()

    def load_recipes(self):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    name = lines[i].strip()
                    ingredients = lines[i + 1].strip().split(', ')
                    instructions = lines[i + 2].strip()
                    self.recipes[name] = {'ingredients': ingredients, 'instructions': instructions}
                    i += 3
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f'Error loading recipes: {e}')  

    def save_recipes(self):
        try:
            with open('recipes.txt', 'w') as file:
                for name, recipe in self.recipes.items():
                    file.write(f'{name}\n')
                    file.write(', '.join(recipe['ingredients']) + '\n')
                    file.write(f'{recipe['instructions']}\n')
        except Exception as e:
            print(f'Error saving recipes: {e}')  

    def add_recipe(self, name, ingredients, instructions):
        if name in self.recipes:
            raise Exception('Recipe already exists')
        self.recipes[name] = {'ingredients': ingredients, 'instructions': instructions}
        self.save_recipes()

    def get_recipe(self, name):
        return self.recipes.get(name)

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()
            return True
        return False