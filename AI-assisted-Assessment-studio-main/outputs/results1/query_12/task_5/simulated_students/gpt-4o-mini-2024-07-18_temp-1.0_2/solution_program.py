def generate_ingredient_report():
    import os
    from collections import defaultdict

    ingredient_count = defaultdict(int)
    
    if not os.path.exists('recipes.txt') or os.path.getsize('recipes.txt') == 0:
        with open('ingredient_report.txt', 'w') as report:
            pass
        return

    with open('recipes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if '|' not in line:
                continue
            recipe, ingredients = line.split('|', 1)
            ingredients = ingredients.strip().split(',')
            
            for ingredient in ingredients:
                ingredient = ingredient.strip()
                ingredient_count[ingredient] += 1
                
    sorted_ingredients = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)
    
    with open('ingredient_report.txt', 'w') as report:
        for ingredient, count in sorted_ingredients:
            report.write(f'{ingredient}: {count}\n')