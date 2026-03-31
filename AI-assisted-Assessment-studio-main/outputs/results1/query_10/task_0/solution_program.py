import os

class RecipeManager:
    def add_recipe(self, name, ingredients, steps):
        try:
            with open('recipes.txt', 'a') as file:
                file.write(f"{name}\n{', '.join(ingredients)}\n{steps}\n")
        except Exception as e:
            print("An error occurred while adding the recipe.")

    def get_recipe(self, name):
        if not os.path.exists('recipes.txt'):
            return "Recipe not found"
        try:
            with open('recipes.txt', 'r') as file:
                lines = file.readlines()
            for i in range(0, len(lines), 3):
                if lines[i].strip() == name:
                    return f"{lines[i].strip()}\nIngredients: {lines[i + 1].strip()}\nSteps: {lines[i + 2].strip()}"
        except Exception as e:
            print("An error occurred while retrieving the recipe.")
        return "Recipe not found"