def generate_ingredient_report():
    import os
    from collections import Counter

    if not os.path.exists('recipes.txt') or os.path.getsize('recipes.txt') == 0:
        open('ingredient_report.txt', 'w').close()
        return

    ingredient_count = Counter()

    with open('recipes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '|' in line:
                parts = line.split('|')
                if len(parts) == 2:
                    ingredients = parts[1].strip().split(',')
                    for ingredient in ingredients:
                        ingredient_count[ingredient.strip()] += 1

    with open('ingredient_report.txt', 'w') as report:
        for ingredient, count in ingredient_count.most_common():
            report.write(f'{ingredient}: {count}\n')
