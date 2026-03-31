class RecipeManager:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.file_name, 'a') as file:
                file.write(name + '\n')
                for ingredient in ingredients:
                    file.write(ingredient + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'An error occurred while adding the recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                in_recipe = False
                recipe_details = ''
               
                for line in lines:
                    if line.strip() == name:
                        in_recipe = True
                        recipe_details += line.strip() + '\n'
                    elif in_recipe:
                        if line.strip() == '':
                            break
                        recipe_details += line.strip() + '\n'
                if recipe_details:
                    return recipe_details.strip()
                else:
                    return 'Recipe not found'
        except Exception as e:
            return f'An error occurred while retrieving the recipe: {e}'