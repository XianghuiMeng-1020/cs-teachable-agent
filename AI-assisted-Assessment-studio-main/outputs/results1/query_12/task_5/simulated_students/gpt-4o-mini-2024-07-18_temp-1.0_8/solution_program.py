def generate_ingredient_report():
    import os
    from collections import defaultdict

    ingredient_count = defaultdict(int)

    if not os.path.isfile('recipes.txt') or os.path.getsize('recipes.txt') == 0:
        open('ingredient_report.txt', 'w').close()
        return

    with open('recipes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '|' in line:
                parts = line.split('|')
                if len(parts) == 2:
                    ingredients = parts[1].strip().split(',')
                    for ingredient in ingredients:
                        ingredient = ingredient.strip()
                        ingredient_count[ingredient] += 1

    sorted_ingredients = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)

    with open('ingredient_report.txt', 'w') as report_file:
        for ingredient, count in sorted_ingredients:
            report_file.write(f'{ingredient}: {count}\n')