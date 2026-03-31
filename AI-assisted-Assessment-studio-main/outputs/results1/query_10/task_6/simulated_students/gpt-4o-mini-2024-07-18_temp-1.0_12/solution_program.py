class RecipeManager:
    def __init__(self):
        self.recipes = {}
        self.load_recipes()

    def load_recipes(self):
        try:
            with open('recipes.txt', 'r') as f:
                lines = f.readlines()
                for i in range(0, len(lines), 3):
                    name = lines[i].strip()
                    ingredients = lines[i + 1].strip().split(', ')
                    instructions = lines[i + 2].strip()
                    self.recipes[name] = (ingredients, instructions)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f'Error loading recipes: {e}')  

    def save_recipes(self):
        try:
            with open('recipes.txt', 'w') as f:
                for name, (ingredients, instructions) in self.recipes.items():
                    f.write(f'{name}\n')
                    f.write(f'{", ".join(ingredients)}\n')
                    f.write(f'{instructions}\n')
        except Exception as e:
            print(f'Error saving recipes: {e}')  

    def add_recipe(self, name, ingredients, instructions):
        if name in self.recipes:
            raise Exception('Recipe already exists.')
        self.recipes[name] = (ingredients, instructions)
        self.save_recipes()  

    def get_recipe(self, name):
        return self.recipes.get(name, None)

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()
            return True
        return False