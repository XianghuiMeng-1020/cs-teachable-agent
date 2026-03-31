class Recipe:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
                if name in content:
                    raise Exception('Recipe already exists.')
        except FileNotFoundError:
            pass

        with open(self.filename, 'a') as file:
            file.write(f'{name}\n')
            for ingredient in ingredients:
                file.write(f'{ingredient}\n')
            file.write(f'{instructions}\n')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise Exception('Recipe file not found.')

        i = 0
        while i < len(lines):
            if lines[i].strip() == name:
                ingredients = []
                i += 1
                while not lines[i].strip().endswith('.'):  # instruction line
                    ingredients.append(lines[i].strip())
                    i += 1
                instructions = lines[i].strip()
                return {'ingredients': ingredients, 'instructions': instructions}
                break
            i += 1

        raise Exception('Recipe not found.')