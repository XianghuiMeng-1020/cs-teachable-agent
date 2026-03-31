class RecipeManager:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.filename, 'a') as f:
                f.write(name + '\n')
                for ingredient in ingredients:
                    f.write(ingredient + '\n')
                f.write(steps + '\n')
                f.write('---\n')
        except Exception as e:
            print(f'Error occurred while adding a recipe: {e}')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                current_name = None
                ingredients = []
                steps = ''

                for line in lines:
                    line = line.strip()
                    if line == '---':
                        if current_name and current_name == name:
                            return {'name': current_name, 'ingredients': ingredients, 'steps': steps}
                        current_name = None
                        ingredients = []
                        steps = ''
                    elif current_name is None:
                        current_name = line
                    elif len(ingredients) < 10:
                        ingredients.append(line)
                    else:
                        steps += line + '\n'

                if current_name and current_name == name:
                    return {'name': current_name, 'ingredients': ingredients, 'steps': steps}

                return 'Recipe not found'
        except Exception as e:
            print(f'Error occurred while retrieving a recipe: {e}')