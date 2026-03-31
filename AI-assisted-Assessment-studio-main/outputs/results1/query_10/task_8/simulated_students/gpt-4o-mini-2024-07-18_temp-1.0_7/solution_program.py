class Recipe:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, instructions):
        if self._recipe_exists(name):
            raise Exception("Recipe with this name already exists.")
        with open(self.filename, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            recipe_data = {}
            current_name = None
            current_ingredients = []
            current_instructions = None
            for line in lines:
                line = line.strip()
                if line:
                    if current_name is None:
                        current_name = line
                    elif not current_instructions:
                        if line != current_name:
                            current_ingredients.append(line)
                        else:
                            continue
                    else:
                        continue
                    if not current_instructions and line == current_name:
                        continue
                if current_name and line != current_name:
                    current_instructions = line
                    if current_name == name:
                        recipe_data['ingredients'] = current_ingredients
                        recipe_data['instructions'] = current_instructions
                        return recipe_data
                    current_name = None
                    current_ingredients = []
                    current_instructions = None
            raise Exception("Recipe not found.")

    def _recipe_exists(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip() == name:
                        return True
            return False
        except FileNotFoundError:
            return False