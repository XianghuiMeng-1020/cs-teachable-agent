class Recipe:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        if self.get_recipe(name) is not None:
            raise Exception('Recipe with this name already exists.')
        with open(self.filename, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        recipe = {'ingredients': [], 'instructions': ''}
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    current_name = lines[i].strip()
                    if current_name == name:
                        i += 1
                        while i < len(lines) and lines[i].strip() != '':
                            recipe['ingredients'].append(lines[i].strip())
                            i += 1
                        if i < len(lines):
                            recipe['instructions'] = lines[i].strip()
                        return recipe
                    else:
                        while i < len(lines) and lines[i].strip() != '':
                            i += 1
                    i += 1
            return None
        except FileNotFoundError:
            return None
        except Exception as e:
            raise Exception('An error occurred while retrieving the recipe: ' + str(e))