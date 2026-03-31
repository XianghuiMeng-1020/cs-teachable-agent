class Recipe:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        try:
            with open(self.file_name, 'r') as f:
                if any(name == line.strip() for line in f):
                    raise Exception('Recipe with this name already exists.')

            with open(self.file_name, 'a') as f:
                f.write(name + '\n')
                for ingredient in ingredients:
                    f.write(ingredient + '\n')
                f.write(instructions + '\n')
        except FileNotFoundError:
            with open(self.file_name, 'w') as f:
                f.write(name + '\n')
                for ingredient in ingredients:
                    f.write(ingredient + '\n')
                f.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as f:
                lines = f.readlines()
                i = 0
                while i < len(lines):
                    if lines[i].strip() == name:
                        recipe = {'ingredients': [], 'instructions': ''}
                        i += 1
                        while i < len(lines) and lines[i].strip() != '':
                            recipe['ingredients'].append(lines[i].strip())
                            i += 1
                        if i < len(lines):
                            recipe['instructions'] = lines[i].strip()
                        return recipe
                    i += 1
            raise Exception('Recipe not found.')
        except FileNotFoundError:
            raise Exception('Recipe file does not exist.')