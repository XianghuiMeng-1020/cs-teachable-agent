class Recipe:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, instructions):
        if self._recipe_exists(name):
            raise Exception(f"Recipe '{name}' already exists.")
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
            raise Exception("No recipes file found.")

        recipe_found = False
        recipe = {'ingredients': [], 'instructions': ''}

        for line in lines:
            stripped_line = line.strip()
            if stripped_line == name:
                recipe_found = True
            elif recipe_found and stripped_line == '':
                break
            elif recipe_found:
                if recipe['instructions'] == '':
                    recipe['instructions'] = stripped_line
                else:
                    recipe['ingredients'].append(stripped_line)

        if recipe_found:
            return recipe
        else:
            raise Exception(f"Recipe '{name}' not found.")

    def _recipe_exists(self, name):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    if line.strip() == name:
                        return True
        except FileNotFoundError:
            return False
        return False