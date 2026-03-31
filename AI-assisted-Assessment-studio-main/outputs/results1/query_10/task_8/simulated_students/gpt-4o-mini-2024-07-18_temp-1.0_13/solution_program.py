class Recipe:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        if self._recipe_exists(name):
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
            i = 0
            while i < len(lines):
                if lines[i].strip() == name:
                    ingredients = []
                    i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].startswith('\n'):
                        ingredients.append(lines[i].strip())
                        i += 1
                    instructions = lines[i].strip() if i < len(lines) else ''
                    return {'ingredients': ingredients, 'instructions': instructions}
                # Skip to the next recipe
                while i < len(lines) and lines[i].strip():
                    i += 1
                i += 1
            raise Exception(f'Recipe with name {name} not found.')
        except FileNotFoundError:
            raise Exception('Recipes file not found.')

    def _recipe_exists(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            for line in lines:
                if line.strip() == name:
                    return True
            return False
        except FileNotFoundError:
            return False
