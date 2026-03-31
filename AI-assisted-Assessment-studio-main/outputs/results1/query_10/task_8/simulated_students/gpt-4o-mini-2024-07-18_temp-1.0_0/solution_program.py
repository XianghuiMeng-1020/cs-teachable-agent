class Recipe:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        if self.get_recipe(name) is not None:
            raise Exception('Recipe with this name already exists.')
        with open(self.file_name, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            return None

        recipe = None
        ingredients = []
        instructions = None
        reading_ingredients = False

        for line in lines:
            line = line.strip()
            if line == '':
                continue
            if not recipe:
                recipe = line
                reading_ingredients = True
            elif reading_ingredients:
                if instructions is None:
                    ingredients.append(line)
                elif instructions is not None:
                    instructions = line
                    reading_ingredients = False
            else:
                if recipe == name:
                    return {'ingredients': ingredients, 'instructions': instructions}
                recipe = line
                ingredients = []
                instructions = None
                reading_ingredients = True
        if recipe == name:
            return {'ingredients': ingredients, 'instructions': instructions}
        return None