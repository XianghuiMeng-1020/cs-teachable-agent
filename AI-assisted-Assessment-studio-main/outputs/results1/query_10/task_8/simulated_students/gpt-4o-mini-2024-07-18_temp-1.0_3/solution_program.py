class Recipe:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        recipes = self._read_recipes()
        if name in recipes:
            raise Exception('Recipe already exists')
        with open(self.filename, 'a') as f:
            f.write(name + '\n')
            for ingredient in ingredients:
                f.write(ingredient + '\n')
            f.write(instructions + '\n')

    def get_recipe(self, name):
        recipes = self._read_recipes()
        if name not in recipes:
            raise Exception('Recipe not found')
        return recipes[name]

    def _read_recipes(self):
        recipes = {}
        try:
            with open(self.filename, 'r') as f:
                content = f.read().strip().split('\n')
                i = 0
                while i < len(content):
                    name = content[i]
                    i += 1
                    ingredients = []
                    while i < len(content) and content[i] != '':
                        ingredients.append(content[i])
                        i += 1
                    if i < len(content):
                        instructions = content[i]
                        recipes[name] = {'ingredients': ingredients, 'instructions': instructions}
                    i += 1
        except FileNotFoundError:
            open(self.filename, 'w').close()
        return recipes
