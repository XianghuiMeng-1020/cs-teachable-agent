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
            print(f'Error while adding recipe: {e}')  # Handle file operation errors

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    recipe_name = lines[i].strip()
                    if recipe_name.lower() == name.lower():
                        ingredients = []
                        i += 1
                        while lines[i].strip() != '':
                            ingredients.append(lines[i].strip())
                            i += 1
                        i += 1  # Skip the empty line after ingredients
                        steps = []
                        while i < len(lines) and lines[i].strip() != '':
                            steps.append(lines[i].strip())
                            i += 1
                        return {'name': recipe_name, 'ingredients': ingredients, 'steps': '\n'.join(steps)}
                    i += 1
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            return f'Error while retrieving recipe: {e}'  # Handle file operation errors
        return 'Recipe not found'