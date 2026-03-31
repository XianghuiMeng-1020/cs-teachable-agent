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
                recipe_name = ''
                ingredients = []
                steps = ''
                reading_ingredients = False
                reading_steps = False
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if recipe_name == '':
                        recipe_name = line
                    elif not reading_ingredients and not reading_steps:
                        if line == '':
                            reading_ingredients = True
                        else:
                            if recipe_name == name:
                                ingredients.append(line)
                    elif reading_ingredients:
                        if line == '':
                            reading_steps = True
                        else:
                            ingredients.append(line)
                    elif reading_steps:
                        if recipe_name == name:
                            steps += line + '\n'
                    if recipe_name == name and reading_steps:
                        break
                if recipe_name == name:
                    return f'Recipe: {recipe_name}\nIngredients: {\n.join(ingredients)}\nSteps: {steps.strip()}'
                else:
                    return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            return f'An error occurred while retrieving the recipe: {e}'