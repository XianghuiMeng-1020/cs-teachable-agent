class RecipeManager:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                for ingredient in ingredients:
                    file.write(ingredient + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'An error occurred while adding the recipe: {e}') 

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                recipe_found = False
                recipe_details = []
                for line in lines:
                    line = line.strip()
                    if line == name:
                        recipe_found = True
                        recipe_details.append(line)
                    elif recipe_found:
                        if line:  # ingredient or step
                            recipe_details.append(line)
                        else:  # empty line indicates end of recipe
                            break
                if recipe_found:
                    return '\n'.join(recipe_details)
                else:
                    return 'Recipe not found'
        except FileNotFoundError:
            return 'Recipe not found'
        except Exception as e:
            print(f'An error occurred while retrieving the recipe: {e}')