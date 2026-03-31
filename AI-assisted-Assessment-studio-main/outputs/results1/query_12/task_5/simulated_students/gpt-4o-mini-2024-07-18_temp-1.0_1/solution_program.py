def generate_ingredient_report():
    import os
    from collections import defaultdict

    ingredient_count = defaultdict(int)

    if not os.path.exists('recipes.txt') or os.stat('recipes.txt').st_size == 0:
        open('ingredient_report.txt', 'w').close()  # Create an empty file
        return

    with open('recipes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '|' not in line:
                continue
            recipe, ingredients_part = line.split('|', 1)
            ingredients = ingredients_part.split(',')
            for ingredient in ingredients:
                ingredient = ingredient.strip()
                ingredient_count[ingredient] += 1

    sorted_ingredients = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)

    with open('ingredient_report.txt', 'w') as report_file:
        for ingredient, count in sorted_ingredients:
            report_file.write(f'{ingredient}: {count}\n')