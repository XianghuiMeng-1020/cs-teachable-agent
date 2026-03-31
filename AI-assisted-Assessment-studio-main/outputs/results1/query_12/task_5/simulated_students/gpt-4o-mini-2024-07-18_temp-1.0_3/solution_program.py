def generate_ingredient_report():
    try:
        with open('recipes.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    ingredient_count = {}

    for line in lines:
        line = line.strip()
        if '|' in line:
            recipe_name, ingredients_str = line.split('|', 1)
            ingredients = ingredients_str.split(',')
            for ingredient in ingredients:
                ingredient = ingredient.strip()
                if ingredient:
                    if ingredient in ingredient_count:
                        ingredient_count[ingredient] += 1
                    else:
                        ingredient_count[ingredient] = 1

    sorted_ingredients = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)

    with open('ingredient_report.txt', 'w') as report_file:
        for ingredient, count in sorted_ingredients:
            report_file.write(f'{ingredient}: {count}\n')