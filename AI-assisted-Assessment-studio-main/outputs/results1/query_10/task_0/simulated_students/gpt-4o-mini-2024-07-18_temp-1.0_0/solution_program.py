class RecipeManager:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'Error occurred while adding recipe: {e}')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    recipe_name = lines[i].strip()
                    if recipe_name == name:
                        i += 1
                        ingredients = []
                        while lines[i].strip() and i < len(lines):
                            ingredients.append(lines[i].strip())
                            i += 1
                        steps = ''
                        while i < len(lines) and lines[i].strip():
                            steps += lines[i].strip() + '\n'
                            i += 1
                        return {'name': recipe_name, 'ingredients': ingredients, 'steps': steps.strip()}
                    i += 1
                return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            print(f'Error occurred while retrieving recipe: {e}')