class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.name + '\n')
            file.write(','.join(self.ingredients) + '\n')
            file.write(self.instructions)

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'r') as file:
                name = file.readline().strip()
                ingredients = file.readline().strip().split(',')
                instructions = file.readline().strip()
                return Recipe(name, ingredients, instructions)
        except Exception:
            return None