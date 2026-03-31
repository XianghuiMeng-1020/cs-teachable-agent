def generate_ingredient_report():
    from collections import defaultdict
    import os

    ingredient_count = defaultdict(int)

    if not os.path.exists('recipes.txt') or os.path.getsize('recipes.txt') == 0:
        open('ingredient_report.txt', 'w').close()
        return

    with open('recipes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '|' not in line:
                continue
            recipe, ingredients = line.split('|', 1)
            ingredients = ingredients.strip()
            if ingredients:
                for ingredient in ingredients.split(','):
                    ingredient = ingredient.strip()
                    ingredient_count[ingredient] += 1

    sorted_ingredients = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)

    with open('ingredient_report.txt', 'w') as report:
        for ingredient, count in sorted_ingredients:
            report.write(f'{ingredient}: {count}\n')
