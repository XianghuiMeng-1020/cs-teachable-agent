class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def add_recipe(self, name, ingredients, instructions):
        if self._recipe_exists(name):
            raise ValueError("Recipe with this name already exists")
        with open('recipes.txt', 'a') as f:
            f.write(f'{name}\n')
            for ingredient in ingredients:
                f.write(f'{ingredient}\n')
            f.write(f'{instructions}\n')

    def get_recipe(self, name):
        try:
            with open('recipes.txt', 'r') as f:
                lines = f.readlines()
            recipe_found = False
            recipe = {}
            current_ingredients = []
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                if i == 0:
                    recipe_name = line
                elif recipe_name == name:
                    if i > 0 and not recipe_found:
                        recipe_found = True
                        current_ingredients.append(line)
                elif recipe_found:
                    if len(current_ingredients) > 0 and line:
                        current_ingredients.append(line)
                    else:
                        recipe['ingredients'] = current_ingredients
                        recipe['instructions'] = line
                        return recipe
            if not recipe_found:
                raise KeyError("Recipe not found")
        except FileNotFoundError:
            raise FileNotFoundError("recipes.txt file not found")

    def _recipe_exists(self, name):
        try:
            with open('recipes.txt', 'r') as f:
                lines = f.readlines()
                if name in lines:
                    return True
            return False
        except FileNotFoundError:
            return False