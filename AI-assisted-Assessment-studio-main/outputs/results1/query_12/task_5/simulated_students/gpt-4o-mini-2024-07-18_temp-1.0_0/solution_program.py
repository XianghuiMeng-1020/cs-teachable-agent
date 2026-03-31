def generate_ingredient_report():
    import os
    from collections import Counter

    if not os.path.exists('recipes.txt') or os.stat('recipes.txt').st_size == 0:
        open('ingredient_report.txt', 'w').close()  # create an empty report
        return

    ingredient_count = Counter()

    with open('recipes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '|' in line:
                recipe, ingredients = line.split('|', 1)
                ingredients = ingredients.strip()
                ingredient_list = [ingredient.strip() for ingredient in ingredients.split(',')]  # list of ingredients
                ingredient_count.update(ingredient_list)

    sorted_ingredients = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)

    with open('ingredient_report.txt', 'w') as report:
        for ingredient, count in sorted_ingredients:
            report.write(f'{ingredient}: {count}\n')