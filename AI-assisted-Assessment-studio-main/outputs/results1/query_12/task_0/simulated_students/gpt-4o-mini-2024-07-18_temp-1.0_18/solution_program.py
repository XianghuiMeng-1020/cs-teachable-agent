def read_ingredients(filename):
    with open(filename, 'r') as file:
        return {line.strip() for line in file}


def read_recipes(filename):
    recipes = {}
    with open(filename, 'r') as file:
        for line in file:
            recipe_name, ingredients = line.strip().split(': ')
            recipes[recipe_name] = ingredients.split(',')
    return recipes


def write_summary_to_file(summary, filename):
    with open(filename, 'w') as file:
        for recipe, status in summary.items():
            file.write(f'{recipe}: {status}\n')


def main():
    pantry = read_ingredients('pantry.txt')
    recipes = read_recipes('recipes.txt')
    summary = {}  
    
    for recipe_name, ingredients in recipes.items():
        available_ingredients = set(ingredients).intersection(pantry)
        if len(available_ingredients) == len(ingredients):
            summary[recipe_name] = 'Fully Prepared'
        elif len(available_ingredients) > 0:
            summary[recipe_name] = 'Partially Missing'
        else:
            summary[recipe_name] = 'Unavailable'

    write_summary_to_file(summary, 'recipe_summary.txt')


if __name__ == '__main__':
    main()