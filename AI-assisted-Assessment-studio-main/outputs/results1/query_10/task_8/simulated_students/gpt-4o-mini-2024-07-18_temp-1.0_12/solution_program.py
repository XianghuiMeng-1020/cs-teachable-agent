class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def add_recipe(self, name, ingredients, instructions):
        if self.recipe_exists(name):
            raise Exception(f'Recipe with the name {name} already exists.')
        with open('recipes.txt', 'a') as file:
            file.write(f'{name}\n')
            for ingredient in ingredients:
                file.write(f'{ingredient}\n')
            file.write(f'{instructions}\n')

    def get_recipe(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                recipe_name = None
                ingredients = []
                instructions = None
                for line in lines:
                    line = line.strip()
                    if recipe_name is None:
                        recipe_name = line
                    elif line == "":
                        instructions = next(lines).strip()
                        if instructions:
                            return {'ingredients': ingredients, 'instructions': instructions}
                        return {'ingredients': ingredients, 'instructions': ''}
                    else:
                        ingredients.append(line)
                if recipe_name == name:
                    return {'ingredients': ingredients, 'instructions': instructions}
                else:
                    raise Exception(f'Recipe with the name {name} does not exist.')
        except FileNotFoundError:
            raise Exception('Recipe file not found.')

    def recipe_exists(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                return any(line.strip() == name for line in lines[::len(lines)])
        except FileNotFoundError:
            return False
