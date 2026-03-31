class Recipe:
    def __init__(self, filepath='recipes.txt'):
        self.filepath = filepath

    def add_recipe(self, name, ingredients, instructions):
        if self.get_recipe(name) is not None:
            raise Exception(f'Recipe with name {name} already exists.')
        with open(self.filepath, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open(self.filepath, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    current_name = lines[i].strip()
                    if current_name == name:
                        i += 1
                        ingredients = []
                        while i < len(lines) and lines[i].strip() != '':
                            ingredients.append(lines[i].strip())
                            i += 1
                        instructions = lines[i].strip() if i < len(lines) else ''
                        return {'ingredients': ingredients, 'instructions': instructions}
                    i += 1
        except FileNotFoundError:
            return None
        return None
