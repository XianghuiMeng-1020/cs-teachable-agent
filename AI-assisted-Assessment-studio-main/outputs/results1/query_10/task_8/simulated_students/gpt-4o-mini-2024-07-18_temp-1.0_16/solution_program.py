class Recipe:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        if self.get_recipe(name) is not None:
            raise Exception(f'Recipe with name {name} already exists.')
        with open(self.filename, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            return None

        current_recipe_name = None
        ingredients = []
        instructions = ''
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if current_recipe_name is None:
                current_recipe_name = line
            elif instructions == '' and line != instructions:
                ingredients.append(line)
            else:
                instructions = line

            if current_recipe_name == name:
                return {'ingredients': ingredients, 'instructions': instructions}
            if instructions:
                current_recipe_name = None
                ingredients = []
                instructions = ''

        return None