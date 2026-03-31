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
            print(f'Error saving recipe: {e}')  

    def get_recipe(self, name):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    if lines[i].strip() == name:
                        i += 1
                        ingredients = []
                        while lines[i].strip():
                            ingredients.append(lines[i].strip())
                            i += 1
                        i += 1  # Skip the blank line after ingredients
                        steps = ''
                        while i < len(lines) and lines[i].strip():
                            steps += lines[i] + '\n'
                            i += 1
                        return {'name': name, 'ingredients': ingredients, 'steps': steps.strip()}
                    i += 1
            return 'Recipe not found'
        except Exception as e:
            return f'Error retrieving recipe: {e}'