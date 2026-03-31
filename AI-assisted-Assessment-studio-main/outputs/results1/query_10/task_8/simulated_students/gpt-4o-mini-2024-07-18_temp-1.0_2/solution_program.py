class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients  
        self.instructions = instructions

    def add_recipe(self, name, ingredients, instructions):
        if self.recipe_exists(name):
            raise Exception("Recipe already exists.")
        with open('recipes.txt', 'a') as file:
            file.write(name + '\n')
            for ingredient in ingredients:
                file.write(ingredient + '\n')
            file.write(instructions + '\n')

    def get_recipe(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    if lines[i].strip() == name:
                        ingredients = []
                        i += 1
                        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('Instructions'):
                            ingredients.append(lines[i].strip())
                            i += 1
                        instructions = lines[i].strip() if i < len(lines) else None
                        return {'ingredients': ingredients, 'instructions': instructions}
                    i += 1
            raise Exception("Recipe not found.")
        except FileNotFoundError:
            raise Exception("Recipe file does not exist.")

    def recipe_exists(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip() == name:
                        return True
        except FileNotFoundError:
            return False
        return False