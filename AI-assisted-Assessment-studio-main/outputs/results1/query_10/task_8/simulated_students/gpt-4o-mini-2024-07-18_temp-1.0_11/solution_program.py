class Recipe:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, instructions):
        if self.get_recipe(name):
            raise ValueError('Recipe with this name already exists.')
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
                    recipe_name = lines[i].strip()
                    if recipe_name == name:
                        ingredients = []
                        i += 1
                        while i < len(lines) and not lines[i].strip().startswith('\t'):
                            ingredients.append(lines[i].strip())
                            i += 1
                        instructions = lines[i].strip() if i < len(lines) else ''
                        return {'ingredients': ingredients, 'instructions': instructions}
                    else:
                        while i < len(lines) and lines[i].strip() != '':
                            i += 1
                    i += 1
        except FileNotFoundError:
            return None
        return None