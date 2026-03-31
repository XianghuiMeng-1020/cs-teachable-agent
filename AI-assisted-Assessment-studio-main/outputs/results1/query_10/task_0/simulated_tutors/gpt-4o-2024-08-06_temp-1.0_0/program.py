class RecipeManager:
    def __init__(self):
        self.file_name = 'recipes.txt'

    def add_recipe(self, name, ingredients, steps):
        try:
            with open(self.file_name, 'a') as file:
                # Write the recipe name
                file.write(f"{name}\n")
                # Join and write ingredients by comma
                file.write(", ".join(ingredients) + "\n")
                # Write the preparation steps
                file.write(f"{steps}\n")
        except Exception as e:
            print(f"An error occurred while adding a recipe: {e}")

    def get_recipe(self, name):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    if lines[i].strip() == name:
                        ingredients = lines[i+1].strip()
                        steps = lines[i+2].strip()
                        return f"{name}\nIngredients: {ingredients}\nSteps: {steps}"
        except FileNotFoundError:
            print("File not found. Creating a new one.")
            open(self.file_name, 'w').close()
            return "Recipe not found"
        except Exception as e:
            print(f"An error occurred while retrieving the recipe: {e}")
        return "Recipe not found"