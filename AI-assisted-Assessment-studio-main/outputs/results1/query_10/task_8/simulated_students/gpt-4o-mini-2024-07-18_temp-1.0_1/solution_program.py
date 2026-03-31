class Recipe:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, instructions):
        try:
            with open(self.filename, 'r') as file:
                if name in [line.strip() for line in file if line.strip()]:
                    raise ValueError('Recipe with this name already exists.')
        except FileNotFoundError:
            pass  # File does not exist, safe to create a new recipe.
        with open(self.filename, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                index = 0
                while index < len(lines):
                    recipe_name = lines[index].strip()
                    index += 1
                    ingredients = []
                    while index < len(lines) and lines[index].strip() != '':
                        ingredients.append(lines[index].strip())
                        index += 1
                    instructions = lines[index].strip() if index < len(lines) else ''
                    index += 1
                    if recipe_name == name:
                        return {'ingredients': ingredients, 'instructions': instructions}
            raise KeyError('Recipe not found.')
        except FileNotFoundError:
            raise FileNotFoundError('The recipe file does not exist.')