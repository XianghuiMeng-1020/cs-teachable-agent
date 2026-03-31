class RecipeManager:
    def __init__(self):
        self.filename = 'recipes.txt'
        self.recipes = {}
        self.load_recipes()

    def load_recipes(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
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
            with open(self.filename, 'w') as file:
                for name, (ingredients, instructions) in self.recipes.items():
                    file.write(f'{name}\n')
                    file.write(', '.join(ingredients) + '\n')
                    file.write(f'{instructions}\n')
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