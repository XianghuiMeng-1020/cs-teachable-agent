class RecipeManager:
    def __init__(self):
        self.filename = 'recipes.txt'
        self.recipes = self._load_recipes()
        
    def _load_recipes(self):
        recipes = {}
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    if lines[i].strip():
                        name = lines[i].strip()
                        ingredients = lines[i + 1].strip()
                        instructions = lines[i + 2].strip()
                        recipes[name] = (ingredients, instructions)
                        i += 3
                    else:
                        i += 1
        except FileNotFoundError:
            pass
        return recipes
        
    def add_recipe(self, name, ingredients, instructions):
        if name in self.recipes:
            raise Exception(f"Recipe '{name}' already exists.")
        self.recipes[name] = (ingredients, instructions)
        with open(self.filename, 'a') as file:
            file.write(f"{name}\n{ingredients}\n{instructions}\n\n")

    def get_recipe(self, name):
        return self.recipes.get(name, None)

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self._save_recipes()
            return True
        return False

    def _save_recipes(self):
        with open(self.filename, 'w') as file:
            for name, (ingredients, instructions) in self.recipes.items():
                file.write(f"{name}\n{ingredients}\n{instructions}\n\n")