class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def to_string(self):
        return f'{self.name}:{','.join(self.ingredients)}'

    @classmethod
    def from_string(cls, recipe_string):
        name, ingredients = recipe_string.split(':')
        ingredients_list = ingredients.split(',')
        return cls(name, ingredients_list)


def save_recipe_to_file(recipe, file_name):
    try:
        with open(file_name, 'a') as file:
            file.write(recipe.to_string() + '\n')
    except Exception:
        pass


def load_recipes_from_file(file_name):
    recipes = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                recipe = Recipe.from_string(line.strip())
                recipes.append(recipe)
    except FileNotFoundError:
        return []
    except Exception:
        return []
    return recipes
