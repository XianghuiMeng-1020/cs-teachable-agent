def generate_ingredient_report():
    import os
    from collections import Counter

    if not os.path.exists('recipes.txt') or os.path.getsize('recipes.txt') == 0:
        open('ingredient_report.txt', 'w').close()
        return

    ingredient_counts = Counter()

    with open('recipes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '|' in line:
                parts = line.split('|')
                if len(parts) > 1:
                    ingredients_part = parts[1].strip()
                    ingredients = ingredients_part.split(',')
                    for ingredient in ingredients:
                        ingredient = ingredient.strip()
                        ingredient_counts[ingredient] += 1

    with open('ingredient_report.txt', 'w') as report:
        for ingredient, count in ingredient_counts.most_common():
            report.write(f'{ingredient}: {count}\n')