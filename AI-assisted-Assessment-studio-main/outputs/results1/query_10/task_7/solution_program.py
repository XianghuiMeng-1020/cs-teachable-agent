class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.name + '\n')
            f.write(','.join(self.ingredients) + '\n')
            f.write(self.instructions)

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                if len(lines) < 3:
                    return None
                name = lines[0].strip()
                ingredients = lines[1].strip().split(',')
                instructions = lines[2].strip()
                return Recipe(name, ingredients, instructions)
        except (IOError, IndexError):
            return None