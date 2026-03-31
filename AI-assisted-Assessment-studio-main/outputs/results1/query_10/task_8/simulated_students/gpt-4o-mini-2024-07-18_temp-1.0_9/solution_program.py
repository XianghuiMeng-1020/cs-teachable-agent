class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def add_recipe(self, name, ingredients, instructions):
        if self.recipe_exists(name):
            raise Exception(f'Recipe with name {name} already exists.')
        with open('recipes.txt', 'a') as file:
            file.write(f'{name}\n')
            for ingredient in ingredients:
                file.write(f'{ingredient}\n')
            file.write(f'{instructions}\n')

    def get_recipe(self, name):
        recipes = self.load_recipes()
        if name not in recipes:
            raise Exception(f'Recipe with name {name} does not exist.')
        return recipes[name]

    def recipe_exists(self, name):
        recipes = self.load_recipes()
        return name in recipes

    def load_recipes(self):
        recipes = {}
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    recipe_name = lines[i].strip()
                    i += 1
                    ingredients = []
                    while i < len(lines) and lines[i].strip() and not lines[i].startswith('\n'):
                        ingredients.append(lines[i].strip())
                        i += 1
                    if i < len(lines):
                        instructions = lines[i].strip()
                        i += 1
                    recipes[recipe_name] = {'ingredients': ingredients, 'instructions': instructions}
        except FileNotFoundError:
            pass
        return recipes