class Recipe:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, instructions):
        with open(self.filename, 'a+') as f:
            f.seek(0)
            recipes = f.readlines()
            if any(line.strip() == name for line in recipes):
                raise Exception('Recipe with this name already exists.')
            f.write(name + '\n')
            for ingredient in ingredients:
                f.write(ingredient + '\n')
            f.write(instructions + '\n')

    def get_recipe(self, name):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                if lines[i].strip() == name:
                    ingredients = []
                    i += 1
                    while i < len(lines) and lines[i].strip() != '':
                        ingredients.append(lines[i].strip())
                        i += 1
                    instructions = lines[i + 1].strip() if i + 1 < len(lines) else ''
                    return {'ingredients': ingredients, 'instructions': instructions}
                i += 1
            raise Exception('Recipe not found.')