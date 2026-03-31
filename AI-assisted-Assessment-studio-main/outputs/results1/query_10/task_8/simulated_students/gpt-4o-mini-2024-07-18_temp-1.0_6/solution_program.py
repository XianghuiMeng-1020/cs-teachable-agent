class Recipe:
    def __init__(self, name, ingredients=None, instructions=''):
        self.name = name
        self.ingredients = ingredients if ingredients is not None else []
        self.instructions = instructions

    def add_recipe(self, name, ingredients, instructions):
        if self.recipe_exists(name):
            raise Exception(f'Recipe with name {name} already exists.')
        with open('recipes.txt', 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                recipe_found = False
                recipe_ingredients = []
                recipe_instructions = ''
                for line in lines:
                    line = line.strip()
                    if line == name:
                        recipe_found = True
                    elif recipe_found:
                        if line == '':
                            continue
                        if recipe_instructions == '' and line not in recipe_ingredients:
                            recipe_ingredients.append(line)
                        elif recipe_instructions == '' and line in recipe_ingredients:
                            continue
                        else:
                            recipe_instructions = line
                            break
                if not recipe_found:
                    raise Exception(f'Recipe with name {name} not found.')
                return {'ingredients': recipe_ingredients, 'instructions': recipe_instructions}
        except FileNotFoundError:
            raise Exception('Recipes file not found.')

    def recipe_exists(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                for line in file:
                    if line.strip() == name:
                        return True
            return False
        except FileNotFoundError:
            return False