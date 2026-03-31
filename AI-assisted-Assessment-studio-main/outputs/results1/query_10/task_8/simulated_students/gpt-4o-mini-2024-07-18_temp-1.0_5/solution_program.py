class Recipe:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, instructions):
        if self.recipe_exists(name):
            raise Exception('Recipe already exists.')
        with open(self.filename, 'a') as file:
            file.write(f'{name}\n')
            for ingredient in ingredients:
                file.write(f'{ingredient}\n')
            file.write(f'{instructions}\n')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            recipe = {}
            i = 0
            while i < len(lines):
                current_name = lines[i].strip()
                if current_name == name:
                    ingredients = []
                    i += 1
                    while i < len(lines) and lines[i].strip() != '':
                        ingredients.append(lines[i].strip())
                        i += 1
                    instructions = lines[i + 1].strip() if i + 1 < len(lines) else ''
                    recipe['ingredients'] = ingredients
                    recipe['instructions'] = instructions
                    return recipe
                i += 2  # Move to the next recipe
            raise Exception('Recipe not found.')
        except FileNotFoundError:
            raise Exception('Recipe file not found.')

    def recipe_exists(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            return any(line.strip() == name for line in lines if line.strip())
        except FileNotFoundError:
            return False