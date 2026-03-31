class RecipeManager:
    def __init__(self, filename='recipes.txt'):
        self.filename = filename

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.filename, 'a') as file:
                file.write(name + '\n')
                file.write('\n'.join(ingredients) + '\n')
                file.write(steps + '\n\n')
        except Exception as e:
            print(f'Error while adding recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                content = file.readlines()
                index = 0
                while index < len(content):
                    recipe_name = content[index].strip()
                    if recipe_name == name:
                        ingredients = []
                        index += 1
                        while index < len(content) and content[index].strip():
                            ingredients.append(content[index].strip())
                            index += 1
                        steps = ""
                        index += 1  # skip the empty line (or goes to next recipe)
                        while index < len(content) and (content[index].strip() or not content[index].isspace() ):
                            steps += content[index].strip() + '\n'
                            index += 1
                        return {'name': recipe_name, 'ingredients': ingredients, 'steps': steps.strip()}
                    index += 1
            return 'Recipe not found'
        except Exception as e:
            return f'Error while retrieving recipe: {e}'