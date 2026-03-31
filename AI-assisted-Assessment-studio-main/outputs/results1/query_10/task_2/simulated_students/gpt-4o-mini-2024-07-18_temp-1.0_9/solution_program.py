class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def to_string(self):
        return f'{self.name}:{" ".join(self.ingredients)}'

    @classmethod
    def from_string(cls, recipe_str):
        name, ingredients_str = recipe_str.split(':')
        ingredients = ingredients_str.split(',')
        return cls(name.strip(), [ingredient.strip() for ingredient in ingredients])


def save_recipe_to_file(recipe, file_name):
    try:
        with open(file_name, 'a') as file:
            file.write(recipe.to_string() + '\n')
    except Exception as e:
        pass


def load_recipes_from_file(file_name):
    recipes = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    recipes.append(Recipe.from_string(line))
    except (FileNotFoundError, IOError):
        return []
    return recipes