class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def to_string(self):
        return f"{self.name}:{','.join(self.ingredients)}"

    @classmethod
    def from_string(cls, recipe_string):
        name, ingredients = recipe_string.split(':')
        ingredient_list = ingredients.split(',')
        return cls(name, ingredient_list)


def save_recipe_to_file(recipe, file_name):
    try:
        with open(file_name, 'w') as file:
            file.write(recipe.to_string())
    except IOError as e:
        print(f"An error occurred while saving the recipe: {e}")


def load_recipes_from_file(file_name):
    recipes = []
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    recipes.append(Recipe.from_string(line))
    except (IOError, FileNotFoundError):
        print("An error occurred while loading recipes. Returning an empty list.")
    return recipes