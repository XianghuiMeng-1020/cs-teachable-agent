class RecipeManager:
    def add_recipe(self, name, ingredients, steps):
        try:
            with open('recipes.txt', 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'Error adding recipe: {e}')

    def get_recipe(self, name):
        try:
            with open('recipes.txt', 'r') as file:
                content = file.read().strip().split('\n\n')
                for recipe in content:
                    lines = recipe.split('\n')
                    recipe_name = lines[0]
                    if recipe_name == name:
                        return recipe
            return 'Recipe not found'
        except Exception as e:
            return f'Error retrieving recipe: {e}'