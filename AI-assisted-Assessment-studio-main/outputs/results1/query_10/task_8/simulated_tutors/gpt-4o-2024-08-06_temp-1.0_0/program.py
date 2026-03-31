class Recipe:
    def __init__(self):
        self.recipes_file = 'recipes.txt'

    def add_recipe(self, name, ingredients, instructions):
        """Add a new recipe to the file, or raise an exception if it exists."""
        try:
            recipes = self._load_recipes()
            if name in recipes:
                raise Exception(f"Recipe '{name}' already exists.")

            # Append new recipe to the file
            with open(self.recipes_file, 'a') as file:
                file.write(f"{name}\n")
                for ingredient in ingredients:
                    file.write(f"{ingredient}\n")
                file.write(f"{instructions}\n")

        except IOError as e:
            print(f"An IOError occurred: {e}")

    def get_recipe(self, name):
        """Retrieve a recipe by name, or raise an exception if not found."""
        try:
            recipes = self._load_recipes()
            if name not in recipes:
                raise Exception(f"Recipe '{name}' does not exist.")
            return recipes[name]

        except IOError as e:
            print(f"An IOError occurred: {e}")

    def _load_recipes(self):
        """Load recipes from the file into a dictionary."""
        recipes = {}
        try:
            with open(self.recipes_file, 'r') as file:
                lines = file.readlines()

                i = 0
                while i < len(lines):
                    name = lines[i].strip()
                    i += 1
                    ingredients = []

                    # Read ingredients
                    while i < len(lines) and lines[i].strip():
                        ingredients.append(lines[i].strip())
                        i += 1

                    instructions = lines[i].strip()
                    i += 1

                    recipes[name] = {
                        'ingredients': ingredients,
                        'instructions': instructions
                    }

        except IOError as e:
            print(f"An IOError occurred: {e}")

        return recipes