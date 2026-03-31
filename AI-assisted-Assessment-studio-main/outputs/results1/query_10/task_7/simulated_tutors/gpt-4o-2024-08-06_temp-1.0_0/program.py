class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                file.write(f"{self.name}\n")
                file.write(f"{','.join(self.ingredients)}\n")
                file.write(f"{self.instructions}\n")
        except IOError as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                if len(lines) != 3:
                    return None
                name = lines[0].strip()
                ingredients = lines[1].strip().split(',')
                instructions = lines[2].strip()
                return Recipe(name, ingredients, instructions)
        except (IOError, IndexError, ValueError) as e:
            print(f"Loading error: {e}")
            return None
