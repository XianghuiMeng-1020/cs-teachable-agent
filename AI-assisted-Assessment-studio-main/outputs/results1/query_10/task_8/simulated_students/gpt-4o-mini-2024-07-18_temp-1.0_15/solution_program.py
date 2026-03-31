class Recipe:
    def __init__(self):
        self.filename = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        if self.get_recipe(name) is not None:
            raise Exception("Recipe with this name already exists.")
        with open(self.filename, 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                current_name = None
                ingredients = []
                instructions = None

                for line in lines:
                    line = line.strip()
                    if current_name is None:
                        current_name = line
                    elif line and instructions is None:
                        ingredients.append(line)
                    elif line and instructions is not None:
                        raise Exception("Invalid file format.")
                    elif line and instructions is None:
                        instructions = line

                    if current_name and instructions:
                        if current_name == name:
                            return {'ingredients': ingredients, 'instructions': instructions}
                        else:
                            current_name = None
                            ingredients = []
                            instructions = None
                return None
        except FileNotFoundError:
            return None
        except Exception as e:
            raise Exception(f"Error reading recipe: {e}")