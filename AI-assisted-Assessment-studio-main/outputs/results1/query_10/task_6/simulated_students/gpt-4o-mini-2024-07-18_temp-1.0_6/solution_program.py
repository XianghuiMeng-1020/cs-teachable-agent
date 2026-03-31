class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename
        self.recipes = {}
        self.load_recipes()

    def load_recipes(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read().strip().split('\n\n')
                for recipe in content:
                    lines = recipe.strip().split('\n')
                    if len(lines) >= 3:
                        name = lines[0].strip()
                        ingredients = lines[1].strip().split(', ')
                        instructions = '\n'.join(lines[2:]).strip()
                        self.recipes[name] = {'ingredients': ingredients, 'instructions': instructions}
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f'Error loading recipes: {e}') 

    def save_recipes(self):
        try:
            with open(self.filename, 'w') as file:
                for name, details in self.recipes.items():
                    file.write(f'{name}\n')
                    file.write(', '.join(details['ingredients']) + '\n')
                    file.write(f'{details['instructions']}\n\n')
        except Exception as e:
            print(f'Error saving recipes: {e}')  

    def add_recipe(self, name, ingredients, instructions):
        if name in self.recipes:
            raise Exception('Recipe already exists')
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