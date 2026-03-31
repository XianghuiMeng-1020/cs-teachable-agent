def read_ingredients(file_name):
    with open(file_name, 'r') as file:
        return {line.strip() for line in file if line.strip()}


def read_recipes(file_name):
    recipes = {}
    with open(file_name, 'r') as file:
        for line in file:
            if ':' in line:
                recipe_name, ingredients = line.strip().split(':', 1)
                recipes[recipe_name.strip()] = [ingredient.strip() for ingredient in ingredients.split(',')]
    return recipes


def evaluate_recipes(recipes, pantry):
    summary = {}  
    for recipe_name, ingredients in recipes.items():
        available_count = sum(1 for ingredient in ingredients if ingredient in pantry)
        if available_count == 0:
            summary[recipe_name] = 'Unavailable'
        elif available_count == len(ingredients):
            summary[recipe_name] = 'Fully Prepared'
        else:
            summary[recipe_name] = 'Partially Missing'
    return summary


def write_summary(summary, output_file):
    with open(output_file, 'w') as file:
        for recipe_name, status in summary.items():
            file.write(f'{recipe_name}: {status}\n')


def main():
    pantry = read_ingredients('pantry.txt')
    recipes = read_recipes('recipes.txt')
    summary = evaluate_recipes(recipes, pantry)
    write_summary(summary, 'recipe_summary.txt')


if __name__ == '__main__':
    main()