class RecipeManager:
    def __init__(self):
        self.recipes = {}
        self.load_recipes()

    def load_recipes(self):
        try:
            with open('recipes.txt', 'r') as f:
                content = f.read().strip().split('\n\n')
                for block in content:
                    lines = block.strip().split('\n')
                    if len(lines) == 3:
                        name, ingredients, instructions = lines
                        self.recipes[name] = (ingredients, instructions)
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty collection.
            self.recipes = {}

    def save_recipes(self):
        with open('recipes.txt', 'w') as f:
            for name, (ingredients, instructions) in self.recipes.items():
                f.write(f"{name}\n{ingredients}\n{instructions}\n\n")

    def add_recipe(self, name, ingredients, instructions):
        if name in self.recipes:
            raise Exception(f"Recipe '{name}' already exists.")
        self.recipes[name] = (ingredients, instructions)
        self.save_recipes()

    def get_recipe(self, name):
        return self.recipes.get(name)

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()
            return True
        return False

# This program makes use of classes and objects to manage states and behaviors related to recipe management.
# It uses exception handling to deal with file-related errors and duplicate recipes.
# File handling is implemented to persist data in 'recipes.txt', demonstrating input/output operations.
# Selection statements are used to make decisions, such as checking if a recipe already exists.