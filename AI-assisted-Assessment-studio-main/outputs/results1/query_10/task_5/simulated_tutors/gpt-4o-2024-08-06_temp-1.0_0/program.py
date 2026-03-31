class Recipe:
    def __init__(self, name, ingredients, cooking_method):
        self.name = name
        self.ingredients = ingredients
        self.cooking_method = cooking_method

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
        else:
            raise ValueError("Ingredient not found")

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                file.write(f"Recipe: {self.name}\n")
                file.write("Ingredients:\n")
                for ingredient in self.ingredients:
                    file.write(f"- {ingredient}\n")
                file.write("Cooking Method:\n")
                file.write(self.cooking_method)
        except IOError:
            print("An error occurred while writing to the file.")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.name = file.readline().strip().split(": ")[1]
                file.readline()  # Skip the "Ingredients:" line
                self.ingredients = []
                line = file.readline().strip()
                while line.startswith('- '):
                    self.ingredients.append(line[2:])
                    line = file.readline().strip()
                self.cooking_method = line.split(": ")[1]
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred while loading from the file:", e)