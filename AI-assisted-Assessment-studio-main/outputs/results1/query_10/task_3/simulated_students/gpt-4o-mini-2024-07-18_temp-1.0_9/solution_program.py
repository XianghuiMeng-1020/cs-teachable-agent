class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                for ingredient in ingredients:
                    file.write(ingredient + '\n')
                file.write('\n')
        except Exception as e:
            print(f'Error adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                recipes = self._parse_recipes(lines)
                return recipes.get(name, None)
        except Exception as e:
            print(f'Error retrieving recipe: {e}')  
            return None

    def delete_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            recipes = self._parse_recipes(lines)

            if name not in recipes:
                return False

            with open(self.filename, 'w') as file:
                for recipe_name, ingredients in recipes.items():
                    if recipe_name != name:
                        file.write(recipe_name + '\n')
                        for ingredient in ingredients:
                            file.write(ingredient + '\n')
                        file.write('\n')
            return True
        except Exception as e:
            print(f'Error deleting recipe: {e}')  
            return False

    def _parse_recipes(self, lines):
        recipes = {}
        current_recipe = None
        current_ingredients = []

        for line in lines:
            line = line.strip()
            if line == '':
                if current_recipe:
                    recipes[current_recipe] = current_ingredients
                    current_recipe = None
                    current_ingredients = []
            elif current_recipe is None:
                current_recipe = line
            else:
                current_ingredients.append(line)

        if current_recipe:
            recipes[current_recipe] = current_ingredients

        return recipes