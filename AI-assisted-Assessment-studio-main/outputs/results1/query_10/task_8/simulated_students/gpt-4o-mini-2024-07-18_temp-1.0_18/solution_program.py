class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    @staticmethod
    def add_recipe(name, ingredients, instructions):
        try:
            with open('recipes.txt', 'r') as file:
                existing_recipes = file.read()  
                if name in existing_recipes:
                    raise Exception('Recipe with this name already exists.')  
        except FileNotFoundError:
            existing_recipes = ''
        with open('recipes.txt', 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    @staticmethod
    def get_recipe(name):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                recipe_found = False
                recipe = {}
                current_name = ''
                current_ingredients = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if not recipe_found:
                        if current_name == '':
                            current_name = line
                        elif current_name == line:
                            recipe_found = True
                        else:
                            current_name = line
                            current_ingredients = []
                    elif recipe_found:
                        if current_name and not current_ingredients:
                            current_ingredients.append(line)
                        else:
                            recipe['instructions'] = line
                            recipe['ingredients'] = current_ingredients
                            return recipe
                if not recipe_found:
                    raise Exception('Recipe not found.')  
        except FileNotFoundError:
            raise Exception('Recipe file does not exist.')