class RecipeManager:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.file_name, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'An error occurred while adding the recipe: {e}') 

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    recipe_name = lines[i].strip()
                    if recipe_name == name:
                        ingredients = []
                        i += 1
                        while i < len(lines) and lines[i].strip() != '':
                            ingredients.append(lines[i].strip())
                            i += 1
                        steps = ''
                        i += 1
                        while i < len(lines) and lines[i].strip() != '':
                            steps += lines[i].strip() + '\n'
                            i += 1
                        return {'name': recipe_name, 'ingredients': ingredients, 'steps': steps.strip()}
                    i += 1
                return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            print(f'An error occurred while retrieving the recipe: {e}')